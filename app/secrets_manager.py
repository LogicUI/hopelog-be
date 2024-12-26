import os
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

def set_env_vars_from_json_str(json_str):
    try:
        secrets_dict = json.loads(json_str)
        
    except json.JSONDecodeError:
        return

    for key, value in secrets_dict.items():
        logging.info("Setting environment variable: %s", key)
        logging.info("Value: %s", value)
        os.environ[key] = str(value)


