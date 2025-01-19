import logging
import json
import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from userUtils.user_utils import get_current_user
from aiModel.ai_therapist import (
    feelings_analysis_agent,
    stream_emotional_therapist_agent,
    emotional_therapist_agent,
    summary_agent,
    analyze_agent,
    title_agent,
)
from redisCache.redis_cache import get_cache, set_cache, reset_cache
from .utils import (
    save_conversation_entry,
    get_conversational_entries,
    delete_conversational_entry,
    get_current_time,
)
from database_init import get_db_connection
from models.conversational_history import ConversationalHistory
from time import perf_counter

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@router.post("/stream-ai-prompt")
def stream_ai_prompt(request: dict, token: str = Depends(get_current_user)):
    user_name = token["user_metadata"]["name"]
    user_message = request.get("user_message")
    conversation_history = request.get("conversation_history")
    completion = emotional_therapist_agent(
        user_message, conversation_history, user_name
    )
    return StreamingResponse(
        stream_emotional_therapist_agent(completion), media_type="text/plain"
    )


@router.delete("/refresh-convo-session")
async def refresh_convo_session(token: str = Depends(get_current_user)):
    user_id = token["sub"]
    reset_cache(user_id)
    return {"message": "Conversation session refreshed successfully"}


@router.put("/update-convo-session")
async def update_convo_session(request: dict, token: str = Depends(get_current_user)):
    user_id = token["sub"]
    conversation_history = request.get("conversation_history")
    set_cache(user_id, json.dumps(conversation_history))
    return {"message": "Conversation session updated successfully"}


@router.get("/get-cached-convo-history")
async def get_cached_convo_history(token: str = Depends(get_current_user)):
    user_id = token["sub"]
    cached_convo_history = get_cache(user_id)
    if not cached_convo_history:
        return {"conversation_history": []}
    return {"conversation_history": json.loads(cached_convo_history)}


@router.post("/save-convo-entry")
async def save_convo_entry(
    conversational_history: ConversationalHistory,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    try:
        timezone = conversational_history.timezone
        logging.info("timezone: %s", timezone)
        current_time = get_current_time(timezone)
        user_id = token["sub"]
        user_name = token["user_metadata"]["name"]
        start_time = perf_counter()
        converse_history = conversational_history.conversation_history
        summary_task = summary_agent(converse_history, user_name)
        analysis_task = analyze_agent(converse_history, user_name)
        title_task = title_agent(converse_history)
        emotional_task = feelings_analysis_agent(converse_history)
        logging.info(f"Emotional task: {emotional_task}")
        summary, analysis, title, emotions = await asyncio.gather(
            summary_task, analysis_task, title_task, emotional_task
        )
        journal_id = save_conversation_entry(
            db_connection, user_id, title, summary, analysis, emotions, current_time
        )
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        logging.info("Time taken to save conversation entry: %s", elapsed_time)
        logging.info("Journal saved successfully with id of %s", journal_id)
        reset_cache(user_id)
        logging.info("Cache reset for user: %s", user_id)
        return {
            "title": title,
            "summary": summary,
            "analysis": analysis,
            "emotions": emotions.get("emotions"),
            "results": f"Journal saved successfully with id of {journal_id}",
        }

    except Exception as e:
        logging.error("Failed to save conversation entry: %s", e)
        raise


@router.get("/conversational-entries")
async def get_all_conversational_entries(
    token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)
):
    try:
        user_id = token["sub"]
        entries = get_conversational_entries(db_connection, user_id)
        return {"entries": entries}
    except Exception as e:
        logging.error("Failed to get conversational entries: %s", e)
        raise


@router.delete("/delete-convo-entry/{journal_id}")
async def delete_convo_entry(
    journal_id: str,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    try:
        user_id = token["sub"]
        logging.info("Deleting journal entry with id: %s", journal_id)
        delete_conversational_entry(db_connection, journal_id)
        entries = get_conversational_entries(db_connection, user_id)
        return {"entries": entries}
    except Exception as e:
        logging.error("Failed to delete journal entry: %s", e)
        raise
