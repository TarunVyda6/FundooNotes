import enum


class ExceptionType(enum.Enum):
    InvalidCredentials = "email or password is incorrect"
    UnVerifiedAccount = "please verify your account first to login"
    EmptyField = "field cannot be empty"
    LengthError = "you are not matching the length requirement"
    ValidationError = "username should contain only alphanumeric characters"
    UnAuthorized = "you are not authorized to perform this operation"


class MyCustomError(Exception):
    def __init__(self, *args):
        self.type = args[0]
        self.message = args[1]


