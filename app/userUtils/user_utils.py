import os
import jwt
import logging
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
load_dotenv()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET,algorithms=["HS256"], audience="authenticated")
        return payload  
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)  
    return user

