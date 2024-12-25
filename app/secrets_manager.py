import os
import json

def set_env_vars_from_json_str(json_str):
    try:
        secrets_dict = json.loads(json_str)
    except json.JSONDecodeError:
        return

    for key, value in secrets_dict.items():
        os.environ[key] = str(value)


