import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    algorithm = JWT_ALGORITHM
    secret = JWT_SECRET

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username, type):
        payload = dict(
			iss=username,
			sub=type
		)
        to_encode = payload.copy()
        if type == "access_token":
            to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=10)})
        else:
            to_encode.update({"exp": datetime.utcnow() + timedelta(hours=720)})

        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def encode_login_token(self, username):
        access_token = self.encode_token(username, "access_token")
        refresh_token = self.encode_token(username, "refresh_token")

        login_token = dict(
			access_token= access_token,
			refresh_token= refresh_token
		)
        return login_token

    def encode_update_token(self, username):
        access_token = self.encode_token(username, "access_token")
        update_token = dict(
			access_token= access_token
		)
        return update_token

    def decode_access_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload['sub'] != "access_token":
                print(payload['sub'])
                raise HTTPException(status_code=401, detail='not an access token')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            print("lo que pasa es que:", e)
            raise HTTPException(status_code=401, detail='Invalid token')

    def decode_refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload['sub'] != "refresh_token":
                print(payload['sub'])
                raise HTTPException(status_code=401, detail='Invalid token')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Sinature has expired')
        except jwt.InvalidTokenError as e:
            print("lo que pasa es que:", e)
            raise HTTPException(status_code=401, detail='Invalid token')
    
    def auth_access_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_access_token(auth.credentials)
        
    def auth_refresh_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_refresh_token(auth.credentials)
