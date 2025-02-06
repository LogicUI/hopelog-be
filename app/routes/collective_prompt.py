import json
import logging
import geocoder
from fastapi import APIRouter, Depends, Request
from redisCache.redis_cache import (
    get_cache,
    set_cache_with_midnight_expiration,
)
from supabase_init import supabase
from database_init import get_db_connection
from models.collective import Collective as collective_prompt


router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@router.get("/daily-prompt")
async def get_daily_prompt(db_connection=Depends(get_db_connection)):
    try:
        if get_cache("daily_prompt"):
            cached_data = get_cache("daily_prompt")
            logging.info("Fetching daily prompt from the cache.")
            return json.loads(cached_data)

        else:
            logging.info("Fetching daily prompt from the database.")
            cursor = db_connection.cursor()

            cursor.execute("SELECT text, emotion FROM prompt ORDER BY RANDOM() LIMIT 1")

            result = cursor.fetchone()
            set_cache_with_midnight_expiration(
                "daily_prompt", json.dumps({"prompt": result[0], "emotion": result[1]})
            )

            if result:
                prompt, emotion = result
                cache_data = json.dumps({"prompt": prompt, "emotion": emotion})
                return {"prompt": prompt, "emotion": emotion}
            else:
                logging.warning("No prompts found in the database.")
                return {"message": "No prompts found"}

    except Exception as e:
        logging.error("Failed to fetch daily prompt: %s", e)
        return {"error": "Failed to fetch daily prompt"}

    finally:
        if "cursor" in locals() and cursor:
            cursor.close()


@router.post("/collective-prompt")
async def create_collective_prompt(
    collective_prompt: collective_prompt,
    request: Request,
    db_connection=Depends(get_db_connection),
):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host

    if client_ip.startswith(("192.", "10.", "172.")) or client_ip in [
        "127.0.0.1",
        "0.0.0.0",
    ]:
        client_ip = "me"

    g = geocoder.ipinfo(client_ip)
    location = g.latlng
    logging.info("Location: %s", location)

    if client_ip == "me":
        client_ip = request.client.host

    data = {
        "user_text": collective_prompt.user_text,
        "emotion": collective_prompt.emotion,
        "ip_address": client_ip,
        "prompt": collective_prompt.prompt,
        "latitude": location[0] if location else None,
        "longitude": location[1] if location else None,
    }

    logging.info("Creating collective prompt: %s", data)
    try:
        cursor = db_connection.cursor()
        query = """
            INSERT INTO collective_prompt (user_text, emotion, ip_address, prompt, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (ip_address)
            DO UPDATE SET
                user_text = EXCLUDED.user_text,
                emotion = EXCLUDED.emotion,
                prompt = EXCLUDED.prompt,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude
            """
        cursor.execute(
            query,
            (
                data["user_text"],
                data["emotion"],
                data["ip_address"],
                data["prompt"],
                data["latitude"],
                data["longitude"],
            ),
        )
        db_connection.commit()
        return {"message": "Collective prompt created successfully"}
    except Exception as e:
        logging.error("Failed to create collective prompt: %s", e)
        return {"error": "Failed to create collective prompt"}
    finally:
        if "cursor" in locals() and cursor:
            cursor.close()


@router.get("/user-prompts")
async def get_user_prompts(db_connection=Depends(get_db_connection)):
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT user_text, emotion, latitude, longitude, prompt FROM collective_prompt"
        )
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return {"prompts": results}
    except Exception as e:
        logging.error("Failed to fetch user prompts: %s", e)
        return {"error": "Failed to fetch user prompts"}
    finally:
        if "cursor" in locals() and cursor:
            cursor.close()
