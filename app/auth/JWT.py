from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.settings import Settings

settings = Settings.parse_obj({})

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

class JWT:
    def create_access_token(data: dict, secret_key: str, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiry: 15 minutes
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

