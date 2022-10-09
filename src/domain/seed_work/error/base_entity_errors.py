from pydantic.errors import PydanticValueError


class InvalidGUIDFormat(PydanticValueError):
    code = 'invalid_id_format'
    msg_template = 'ID ({id}) must be 36 character long UUID.'


class InvalidIDFormat(PydanticValueError):
    code = 'invalid_id_format'
    msg_template = 'ID ({id}) must be an integer greater than 0.'


class InvalidID(PydanticValueError):
    code = 'invalid_id'
    msg_template = 'Given ID ({id}) is invalid for the requested resource: {resource}'


class InvalidToken(PydanticValueError):
    code = 'invalid_token'
    msg_template = 'Given token is invalid.'
