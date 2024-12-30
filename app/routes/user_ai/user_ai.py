import logging
from typing import List, Dict
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from userUtils.user_utils import verify_token, get_current_user 
from aiModel.ai_therapist import stream_emotion_analysis_response, summary_agent ,analyze_agent
from models.chat_response import ChatResponse
from database_init import get_db_connection
from models.conversational_history import ConversationalHistory

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@router.get("/ai-prompt")
def get_user(token: str = Depends(get_current_user)):
    user_id = token["sub"]    
    
    return {"user_id": user_id}


@router.post("/stream-ai-prompt")
async def stream_ai_prompt(request: dict, token: str = Depends(get_current_user)):
    """
    Endpoint to stream AI prompt responses.
    """

    user_name = token["user_metadata"]["name"]
    user_message = request.get("user_message")
    conversation_history = request.get("conversation_history")
    response_generator = await stream_emotion_analysis_response(user_message, conversation_history, user_name)

    return StreamingResponse(response_generator, media_type="text/plain")
   
@router.post("/save-convo-entry")
async def save_convo_entry(conversational_history: ConversationalHistory, token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)):
    try:
         user_id = token["sub"]
         converse_history = conversational_history.conversation_history
         summary =  await summary_agent(converse_history)
         analysis = await analyze_agent(converse_history)
         logging.info("summary %s", summary)
         logging.info("analysis %s", analysis)
         return {
             "summary": summary,
             "analysis": analysis
         }
    
    except Exception as e:
        logging.error("Failed to save conversation entry: %s", e)
        raise HTTPException(status_code=500, detail="Failed to save conversation entry")