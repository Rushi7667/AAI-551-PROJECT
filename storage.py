"""
Storage utilities for loading and saving JSON files.
"""
import json
import os


def load_json(filename, default=None):
    """
    Load data from a JSON file.
    
    Args:
        filename (str): Path to the JSON file.
        default: Default value if file doesn't exist or is invalid.
    
    Returns:
        The loaded JSON data, or the default value if file doesn't exist.
    """
    if not os.path.exists(filename):
        return default if default is not None else {}
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default if default is not None else {}


def save_json(filename, data):
    """
    Save data to a JSON file.
    
    Args:
        filename (str): Path to the JSON file.
        data: Data to save as JSON.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
