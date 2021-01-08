from services.exceptions import (MyCustomError, ExceptionType)


class Validation:
    def validate_data(data: dict) -> object:
        """
        it takes data as input and returns boolean value
        :rtype: boolean
        """
        if 'email' not in data or data['email'] is '':
            raise MyCustomError(ExceptionType.EmptyField, "email field should not be empty")
        if 'password' not in data or data['password'] is '':
            raise MyCustomError(ExceptionType.EmptyField, "password field should not be empty")
        return True

    def validate_register(data: dict) -> object:
        '''
        this method takes dictionary data as input and it validates the length of characters
        :return: True if the data is valid. else it raises LengthError Exception.
        '''
        if len(data['email']) > 50:
            raise MyCustomError(ExceptionType.LengthError, "email maximum length should be 50 character")
        if len(data['password']) > 68 or len(data['password']) <= 6:
            raise MyCustomError(ExceptionType.LengthError, "password length should be between 6 to 50 character")
        if len(data['last_name']) > 20:
            raise MyCustomError(ExceptionType.LengthError, "lastname maximum length should be 20 character")
        if len(data['user_name']) > 20:
            raise MyCustomError(ExceptionType.LengthError, "username maximum length should be 20 character")
        return True
