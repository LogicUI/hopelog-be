import os
import requests
from fastapi import APIRouter, HTTPException
from .email_request import EmailRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/send-email")
async def send_email(email_request: EmailRequest):
    """Send email using Mailgun API"""
    try:
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_url = os.getenv("MAILGUN_URL")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")

        if not mailgun_api_key:
            logging.info("MAILGUN_API_KEY not found")
            raise HTTPException(status_code=500, detail="server error")

        response = requests.post(
            mailgun_url,
            auth=("api", mailgun_api_key),
            timeout=10,
            data={
                "from": f"HopeLog <mailgun@{mailgun_domain}>",
                "to": "johnwee35@gmail.com",
                "subject": email_request.title,
                "text": email_request.message,
            },
        )

        if response.status_code == 200:
            logger.info("Email sent successfully to johnwee35@gmail.com")
            return {"message": "Your message have been sent successfully"}
        else:
            logger.error(f"Failed to send email: {response.text}")
            raise HTTPException(
                status_code=response.status_code, detail="Failed to send email"
            )

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
