"""This file contains the FastAPI code for the authentication API. 
It contains the following endpoints:"""
import os
import logging
import secrets
import hashlib
import base64
from models.user import User
from models.signIn import SignIn
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import AuthError, AuthApiError
from dotenv import load_dotenv
from supabase_init import supabase
from routes.collective_prompt import router 
from secrets_manager import set_env_vars_from_json_str

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
)

logger = logging.getLogger("BasicLogger")

load_dotenv()
app = FastAPI()
app.include_router(router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://build-with-ai-hackaton-fe.vercel.app/", "https://build-with-ai-hackaton-fe.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.middleware("http")
async def log_routes(request: Request, call_next):
    logging.info("Request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    return response



def generate_code_verifier():
    return secrets.token_urlsafe(64)  

def generate_code_challenge(code_verifier):
    sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip("=")
    
@app.get("/")
def health():
    """Check the health status of the API"""
    logger.info("Health check")
    return {"status": "ok"}
    
@app.get("/health")
def health_check():
    """Check the health status of the API"""
    logger.info("Health check")
    return {"status": "ok"}


@app.post("/auth/signup")
def sign_up(user: User):
    """used to sign up a user"""
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name,
                    "age": user.age
                }
            }
        })
        logger.info("Response %s", str(response))
        return {
            "message": "User signed up successfully. Please check your email for verification",
            "data": response
        }
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail="Supabase API error: " + str(e)) from e
    except AuthError as e:
        raise HTTPException(status_code=400, detail="Supabase Auth error: " + str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e)) from e

@app.post("/auth/signin")
def sign_in(user: SignIn):
    """used to sign in a user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {"message": "User signed in successfully", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    
@app.get("/auth/verify")
def verify_session(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return {"is_logged_in": False, "message": "Authorization header missing or invalid"}
    token = authorization.split(" ")[1]
    try:
        user_response = supabase.auth.get_user(token)
        return {
            "is_logged_in": True,
            "user": user_response 
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.post("/auth/logout")
def log_out():
    """used to log out a user"""
    try:
        supabase.auth.sign_out()
        return {"message": "User logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("Unhandled http exception: %s at %s", exc, request.url)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s at %s", exc, request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unhandled exception: {str(exc)}"},
    )