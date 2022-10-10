import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import drop_database, create_database, database_exists
from datetime import datetime
# we should set environment as test before imports
import os

os.environ["ENVIRONMENT"] = "test"

from src.api.injection import ContainerManager
from src.app import create_app
from src.infrastructure.db.db_manager import DBManager


@pytest.fixture(scope="session")
def monkey_session():
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope='session')
def app(monkey_session):
    monkey_session.setenv('ENVIRONMENT', 'test')
    monkey_session.setenv('MYSQL_DB_NAME', 'adjust_test')

    _app = create_app()

    yield _app

    ContainerManager.unwire_containers()


@pytest.fixture(scope='session')
def client(app: Flask):
    app.testing = True  # Must be true to PROPAGATE_EXCEPTIONS
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture(scope='session')
def db(app: Flask):
    db_name = app.config.get('MYSQL_DB_NAME')
    if db_name != 'adjust_test':
        raise Exception('Tests should be run on the test database only.')

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)
    DBManager.metadata.create_all(DBManager.engine)
    session = DBManager.new_session()
    seed_data(session)

    yield DBManager

    drop_database(db_uri)


@pytest.fixture(scope='class')
def db_session(db: DBManager):
    connection = DBManager.engine.connect()
    transaction = connection.begin()

    DBManager.session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )

    # Make sure DBManager returns this session when new_session is called
    session: Session = DBManager.session_factory()
    DBManager.new_session = lambda: session
    DBManager.new_scoped_session = lambda: session
    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def uow():
    return ContainerManager.repositories.unit_of_work()


def seed_data(session: Session):
    from src.domain.adjust_data.entities.data_table import DataTable as DomainDataTable
    from src.infrastructure.entities.adjust_management.data_table import DataTable
    _data = DomainDataTable.create_data(clicks=111,
                                        _date=datetime(2017, 6, 15).date(),
                                        channel="unityads",
                                        country="US",
                                        os="ios",
                                        impressions=100,
                                        installs=200,
                                        spend=202.2,
                                        revenue=40)
    session.add(DataTable.from_dict(_data.to_orm()))

    session.execute('SET sql_mode = NO_ENGINE_SUBSTITUTION')
    session.commit()
