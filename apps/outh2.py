from jose import JWTError, jwt
from datetime import datetime, timedelta


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    secret_key = "your_secret_key"  # Replace with your own secret key
    expires = datetime.now() + expires_delta
    encoded_jwt = jwt.encode(data, secret_key, algorithm="HS256")
    return encoded_jwt