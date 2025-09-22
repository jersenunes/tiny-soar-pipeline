import json
import os
from src.utils import add_timeline

def ingest_alert(alert_file_path:str) -> dict:
    if not os.path.isfile(alert_file_path):
        raise Exception(f"Alert file {alert_file_path} not found")        

    with open(alert_file_path, 'r') as f:
        alert_data = json.load(f)
    
    details = f"Alert {alert_data.get('alert_id')} ingested from source {alert_data.get('source')}"
    
    timeline = add_timeline('ingest', details)    
    
    alert_data.update({'timeline': timeline})

    return alert_data
