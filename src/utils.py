# type: ignore
import json
import os
import yaml
from configs.settings import *
from datetime import datetime
from typing import Dict, List
from pathlib import Path


"""
The utils module provides utility functions for file I/O and timeline management.  
It ensures safe persistence of artifacts and robust reading of configuration files.  
These helpers abstract low-level operations, supporting reliability across all pipeline stages. 
"""


def write_a_file(path:Path, actions:List[Dict]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding='UTF-8') as file:
            for action in actions:
                file.write(str(action) + "\n")
    except Exception as e:
        print(f"Error saving file: {e}")


def save_a_json(path:Path, text:dict) -> None:
    try:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as file:            
            json.dump(text, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving json file: {e}")


def add_timeline(stage:str, details:str) -> Dict:
    try:
        time_stamp = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

        return {
            'stage': stage,
            'ts': time_stamp,
            'details': details
        }
    except Exception as e:
        print(f"Error adding timeline: {e}")
    

def read_a_json_file(path:Path | str) -> Dict:
    try:
        with open(path, 'r') as file:
            json_file = json.load(file)
        return json_file
    except FileNotFoundError:
        print(f"File not found: {path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON {path}: {e}")
        return {}


def read_a_yaml_file(yaml_path: Path) -> Dict:
    try:
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:        
        print(f"File not found: {path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error decoding YAML {path}: {e}")
        return {}


def get_files(path:Path, file_name:str) -> str:
    try:
        if not path.exists():
            return ""
        for index, file in enumerate(os.listdir(path), start=1):
            if file_name in file:
                return file
        return ""
    except Exception as e:
        print(f"Error retrieving files: {e}")