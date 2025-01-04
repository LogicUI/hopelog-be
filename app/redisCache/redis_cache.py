import redis 
import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
import threading


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

REDIS_HOST = os.getenv('REDIS_HEROKU_HOST', 'redis') 
REDIS_PORT = os.getenv('REDIS_HEROKU_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_URL = os.getenv('REDIS_URL', 'redis:6379')


# Initialize Redis client
redis_client = redis.from_url(
        REDIS_URL,
        health_check_interval=10,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        socket_keepalive=True,
        ssl_cert_reqs='none'             
    )

def set_cache(key: str, value: str, ttl: int = None):
    """
    Stores a key in Redis with an optional expiration time.
    """
    try:
        if ttl:
            redis_client.set(key, value, ex=ttl)  
            logging.info("Key '%s' set with value '%s' and will expire in %d seconds.", key, value, ttl)
        else:
            redis_client.set(key, value)
            logging.info("Key '%s' set with value '%s' with no expiration.", key, value)
    except Exception as e:
        logging.error("Failed to set key '%s': %s", key, e)

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
    # Connection to Redis
    r = redis.from_url(
        REDIS_URL,
        health_check_interval=10,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        socket_keepalive=True,
        ssl_cert_reqs='none'             
    )
    
    # Test the connection
    pong = r.ping()
    if pong:
        logging.info("Connected to Redis server!")

    # Create a PubSub instance
    p = r.pubsub()

    p.subscribe('test')

    def redis_auto_check(p):
        t = threading.Timer(5, redis_auto_check, [p])
        t.start()
        p.check_health()

    redis_auto_check(p)

except redis.ConnectionError as e:
    logging.error(f"Could not connect to Redis: {e}")