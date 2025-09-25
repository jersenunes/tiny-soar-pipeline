from src.utils import add_timeline, read_a_json_file

def ingest_alert(alert_file_path:str) -> dict:
    """
    The ingest module attempts to ingest a JSON file.
    If the file does not exist, the process exits with an error message.
    Additionally, it adds a timeline to ensure traceability.
    """

    alert_data = read_a_json_file(alert_file_path)

    if not alert_data:
        raise Exception(f"Alert data is empty!")  
    
    details = f"Alert {alert_data.get('alert_id')} ingested from source {alert_data.get('source')}"
    
    timeline = add_timeline('ingest', details)    
    
    alert_data.update({'timeline': timeline})

    return alert_data
