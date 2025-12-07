
import json
import os


def load_json(filename, default=None):
  
    if not os.path.exists(filename):
        return default if default is not None else {}
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default if default is not None else {}


def save_json(filename, data):
  
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
