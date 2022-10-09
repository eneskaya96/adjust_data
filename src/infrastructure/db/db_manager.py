import threading
from typing import Callable, Optional

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from src.configs.config_manager import ApiConfigManager
from src.infrastructure.mappings.map_manager import MapManager


class DBManager:
    engine: Engine
    session_factory: Callable[..., Session]
    scoped_session_factory: Callable[..., Session]
    metadata: MetaData

    _scoped_session: Optional[Callable[..., Session]] = None

    @classmethod
    def start_db(cls, app: Flask) -> None:
        config = ApiConfigManager.config
        cls.engine = create_engine(
            config.SQLALCHEMY_DATABASE_URI,
            pool_recycle=config.DB_POOL_RECYCLE,
            max_overflow=config.DB_MAX_OVERFLOW,
            pool_size=config.DB_POOL_SIZE,
            pool_timeout=config.DB_POOL_TIMEOUT,
            pool_pre_ping=True
        )
        cls.session_factory = sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=cls.engine
        )
        cls.scoped_session_factory = sessionmaker(
            bind=cls.engine
        )

        cls.metadata = MapManager.map_entities()

        # Use flask-SQLAlchemy and flask-Migration for migration
        with app.app_context():
            db = SQLAlchemy(metadata=cls.metadata)
            db.init_app(app)

            migration = Migrate()
            migration.init_app(app, db)

            if ApiConfigManager.config.ENVIRONMENT != 'test' and not database_exists(cls.engine.url):
                create_database(cls.engine.url, encoding='utf8mb4')

    @classmethod
    def new_session(cls) -> Session:
        return cls.session_factory()

    @classmethod
    def new_scoped_session(cls) -> Session:
        if cls._scoped_session is None:
            cls._scoped_session = scoped_session(cls.scoped_session_factory, threading.get_ident)
        return cls._scoped_session()
