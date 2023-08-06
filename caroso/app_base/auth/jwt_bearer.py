from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app_base.auth.jwt_handler import decode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer,self).__init__(auto_error= auto_error)
        

    async def __call__(self, request: Request):
        
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            
            if not credentials.scheme == "Bearer":
                return HTTPException(status_code = 403, details = "Invalid authentication scheme!")
            if not self.verify_jwt(credentials.credentials):
                return HTTPException(status_code = 403, details = "Invalid or Expired Token!")
            return credentials.credentials
        else:
            return HTTPException(status_code = 403, details = "Invalid or Expired Token!")

    def verify_jwt(self, jwt_token: str):
        isTokenValid: bool = False 
        payload = decode_jwt(jwt_token)
        print(payload)
        if payload:
            isTokenValid = True
        return isTokenValid