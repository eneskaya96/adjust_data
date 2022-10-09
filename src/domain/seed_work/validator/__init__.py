from src.domain.seed_work.error.base_entity_errors import InvalidGUIDFormat, InvalidIDFormat


def check_guid(guid: str) -> str:
    if len(guid) == 36:
        return guid
    raise InvalidGUIDFormat(id=guid)


def check_id(v: int) -> int:
    if not isinstance(v, int) or v <= 0:
        raise InvalidIDFormat(id=v)
    return v
