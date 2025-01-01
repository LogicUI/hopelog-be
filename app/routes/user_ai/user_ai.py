import logging
import json
import asyncio
from typing import List, Dict
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from userUtils.user_utils import verify_token, get_current_user 
from aiModel.ai_therapist import stream_emotion_analysis_response, summary_agent ,analyze_agent, title_agent
from models.chat_response import ChatResponse
from .utils import save_conversation_entry, get_conversational_entries , delete_conversational_entry
from database_init import get_db_connection
from models.conversational_history import ConversationalHistory
from time import perf_counter

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
         start_time = perf_counter()
         converse_history = conversational_history.conversation_history
         saved_convo_history = json.dumps(converse_history)
         summary_task =   summary_agent(converse_history)
         analysis_task =  analyze_agent(converse_history)
         title_task =  title_agent(converse_history)
         summary, analysis, title = await asyncio.gather(summary_task, analysis_task, title_task)
         journal_id = save_conversation_entry(db_connection, user_id, title, summary, analysis)
         end_time = perf_counter()
         elapsed_time = end_time - start_time
         logging.info("Time taken to save conversation entry: %s", elapsed_time)
         logging.info(f"Journal saved successfully with id of {journal_id}")
         return {
             "title": title,
             "summary": summary,
             "analysis": analysis,
             "results": f"Journal saved successfully with id of {journal_id}"
         }
    
    except Exception as e:
        logging.error("Failed to save conversation entry: %s", e)
        raise

@router.get("/conversational-entries")
async def get_all_conversational_entries(token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)):
    try:
        user_id = token["sub"]
        entries = get_conversational_entries(db_connection, user_id)
        return {"entries": entries}
    except Exception as e:
        logging.error("Failed to get conversational entries: %s", e)
        raise      


@router.delete("/delete-convo-entry/{journal_id}")
async def delete_convo_entry(journal_id: str, token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)):
  try:
        user_id = token["sub"]
        logging.info('Deleting journal entry with id: %s', journal_id)
        delete_conversational_entry(db_connection, journal_id)
        entries = get_conversational_entries(db_connection, user_id)
        return {"entries": entries}
  except Exception as e:
        logging.error("Failed to delete journal entry: %s", e)
        raise
         