# type: ignore
from datetime import datetime
from typing import Dict
from configs.settings import *
from src.utils import read_a_yaml_file, add_timeline


def add_action(type:str, target:str, result:str) -> Dict:
    time_stamp = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    
    if target and '-' in target:
        target = target.split('-')[1]

    return {
        'type': type,
        'target': f'Device:{target}',
        'result': result,
        'ts': time_stamp
    }


def respond_alert(incident: Dict) -> Dict:
    """
    The respond module automates response actions based on incident severity and allowlist configurations.
    It supports isolating devices not present in the allowlist when the severity is equal to or greater than 70.
    Response actions are appended to the incident with timestamps and tracked in the incident timeline.
    """

    severity = incident.get('triage', {}).get('severity', 0)
    device_id = incident.get('asset', {}).get('device_id')
    device_allowed = read_a_yaml_file(ALLOWLISTS).get('assets', {}).get('device_ids', [])

    if severity >= 70 and device_id not in device_allowed:
        incident.setdefault('actions', []).append(add_action('isolate', device_id, 'isolated'))
        details = f"Severity={severity}, device_id={device_id} isolated"
    else:
        details = f"No device isolated (severity={severity}, device_id={device_id})"

    timeline = add_timeline('respond', details)
    
    incident['timeline'].extend(timeline if isinstance(timeline, list) else [timeline])

    return incident