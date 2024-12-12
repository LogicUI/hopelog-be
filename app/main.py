"""This file contains the FastAPI code for the authentication API. 
It contains the following endpoints:"""
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
)

logger = logging.getLogger("BasicLogger")

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://build-with-ai-hackaton-fe.vercel.app/"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.middleware("http")
async def log_routes(request: Request, call_next):
    logging.info("Request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    return response


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")

logger.info("Supabase URL: %s", SUPABASE_URL)
logger.info("Supabase Key: %s", SUPABASE_ANON_KEY)
logger.info("Frontend URL: %s", FRONTEND_URL)

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Supabase URL or Key is missing")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class User(BaseModel):
    """user class to define the user model"""
    email: str
    password: str
    
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
                "email_redirect": f"{FRONTEND_URL}/verify"
            }
        })
        logger.info("Response %s", str(response))
        return {
            "message": "User signed up successfully. Please check your email for verification",
            "data": response
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.post("/auth/signin")
def sign_in(user: User):
    """"used to sign in a user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {"message": "User signed in successfully", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    
@app.get("/auth/verify")
def verify_session(token: str):
    """used to verify a user's session"""
    try:
        user = supabase.auth.get_user(token)
        if not user:
            return {"is_logged_in": False, "message": "Session expired or invalid"}
        return {"is_logged_in": True, "user": user}
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

@app.get("/auth/oauth-login")
async def oauth_login():
    """used to log in a user via OAuth"""
    try:
        response = supabase.auth.sign_in_with_oauth({
                "provider": 'google',
                "options": {
                    "redirect_to": f"{FRONTEND_URL}"
                }
            })
        return {"message": "User signed in successfully", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e



@app.exception_handler(HTTPException)
async def http_exception_handler(exc: HTTPException):
    """handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception):
    """handle global exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unhandled exception: {str(exc)}"},
    )
