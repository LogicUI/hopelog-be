import redis 
import logging
from datetime import datetime, timedelta


REDIS_HOST='redis'
REDIS_PORT=6379

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def calculate_ttl_to_midnight() -> int:
    """
    Calculates the time-to-live (TTL) in seconds until midnight.
    """
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    ttl = (midnight - now).seconds
    logging.debug("Calculated TTL to midnight: %d seconds", ttl)
    return ttl

def set_cache_with_midnight_expiration(key: str, value: str):
    """
    Stores a key in Redis with an expiration time set to midnight.
    """
    try:
        ttl = calculate_ttl_to_midnight()
        redis_client.set(key, value, ex=ttl)  # 'ex' sets the expiration in seconds
        logging.info("Key '%s' set with value '%s' and will expire in %d seconds (by midnight).", key, value, ttl)
    except Exception as e:
        logging.error("Failed to set key '%s': %s", key, e)

def reset_cache_at_midnight(key: str):
    """
    Resets a key in Redis with an expiration time set to midnight.
    """
    try:
        ttl = calculate_ttl_to_midnight()
        redis_client.set(key, "", ex=ttl)  # Set an empty value and reset TTL
        logging.info("Key '%s' reset with an empty value and will expire in %d seconds (by midnight).", key, ttl)
    except Exception as e:
        logging.error("Failed to reset key '%s': %s", key, e)

def reset_cache(key: str):
    """
    Resets a key in Redis.
    """
    try:
        redis_client.delete(key)
        logging.info("Key '%s' deleted.", key)
    except Exception as e:
        logging.error("Failed to delete key '%s': %s", key, e)


def get_cache(key: str) -> str:
    """
    Retrieves the value of a key from Redis.
    """
    try:
        value = redis_client.get(key)
        if value is None:
            logging.info("Key '%s' does not exist.", key)
        else:
            logging.info("Retrieved value for key '%s': %s", key, value)
        return value
    except Exception as e:
        logging.error("Failed to retrieve key '%s': %s", key, e)
        return None

try:
    # Connect to Redis
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    # Test the connection
    pong = redis_client.ping()
    if pong:
        logging.info("Connected to Redis server!")

    # Example: Set and get a value
    redis_client.set("key", "value")
    value = redis_client.get("key")
    logging.info(f"Stored value for 'key': {value}")

except redis.ConnectionError as e:
    logging.info(f"Could not connect to Redis: {e}")