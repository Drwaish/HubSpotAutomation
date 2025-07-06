''' Helper function for smooth running'''
import json

def read_json(filepath: str):
    """
    Reads a JSON file and returns its contents as a Python dictionary.
    """
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


    