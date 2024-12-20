from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from. import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

secret_key = settings.secret_key
algorithm1 = settings.algorithm
access_token1 = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=access_token1)):
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm1)
    return encoded_jwt

def verify_token(token: str, credential_exception):
    
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm1)
        id: str = decoded_token.get("user_id")
        if id is None:
            raise credential_exception()
        #return decoded_token
        token_data = schemas.tokendata(id = id)
        return token_data
    except JWTError:
        raise credential_exception
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="could not validate credentials",headers={"WWW-Authenticate":  "bearer"})

    return verify_token(token, credential_exception)