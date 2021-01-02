class MyExceptions(Exception):
    pass


class InvalidCredentials(MyExceptions):
    def __init__(self, message):
        self.message = message


class UnVerifiedAccount(MyExceptions):
    def __init__(self, message):
        self.message = message


class EmptyField(MyExceptions):
    def __init__(self, message):
        self.message = message


class LengthError(MyExceptions):
    def __init__(self, message):
        self.message = message


class ValidationError(MyExceptions):
    def __init__(self, message):
        self.message = message


class UnAuthorized(MyExceptions):
    def __init__(self, message):
        self.message = message
