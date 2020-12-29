import jwt
from decouple import config


class Encrypt:
    """
    this class is used for encoding and decoding the token
    """

    @staticmethod
    def decode(token):
        """
        this method is used for decoding the token
        """
        return jwt.decode(token, config('ENCODE_SECRET_KEY'), algorithms=["HS256"])

    @staticmethod
    def encode(user_id):
        """
        this method is used for encoding the token
        """
        return jwt.encode({"id": user_id}, config('ENCODE_SECRET_KEY'), algorithm="HS256").decode('utf-8')
