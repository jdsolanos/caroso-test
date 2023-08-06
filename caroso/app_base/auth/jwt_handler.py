import time
from jwt import decode, encode, exceptions
from fastapi.responses import JSONResponse
#from decouple import config
import os
JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")

#returns the generated token
def token_response(token:str):
    return{
        "access_token":token
    }

#function used for signing the jwt string

def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time()+ 600
    }
    print(JWT_ALGORITHM)
    print(JWT_SECRET)
    token = encode(payload, key=JWT_SECRET,algorithm=JWT_ALGORITHM,headers={"alg":JWT_ALGORITHM})
    return token_response(token)

def decode_jwt(token:str):
    try:
        decode_token = decode(token,key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(decode_token)
        return decode_token if decode_token['expiry']>= time.time() else None
    except:
        return{}
    
def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        else:
            decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except exceptions.DecodeError:
        return JSONResponse(content={"message":"Invalid TOken"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message":"TOken expired"}, status_code=401)