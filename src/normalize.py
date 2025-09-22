# type: ignore
import uuid
from typing import Dict
from src.utils import add_timeline


def normalize_alert(alert_ingested: Dict) -> Dict:
    incident_id = str(uuid.uuid4())

    timeline = [alert_ingested['timeline']]
    alert_ingested.pop('timeline')

    asset_data = alert_ingested.get('asset', {})
    asset = {
        'device_id': asset_data.get('device_id', 'Null'),
        'hostname': asset_data.get('hostname', 'Null'),
        'ip': asset_data.get('ip', 'Null')
    }
    
    indicators_data = alert_ingested.get('indicators', {})
    indicators = []
    for ioc_type in ['ipv4', 'domains', 'urls', 'sha256']:
        values = indicators_data.get(ioc_type, [])
        for v in values:
            indicators.append({'type': ioc_type, 'value': v})
    
    incident = {
        'incident_id': incident_id,
        'source_alert': alert_ingested,
        'asset': asset,
        'indicators': indicators,
        'timeline': timeline
    }

    details = f"Extracted {len(indicators)} indicator(s) and {'1 asset' if asset['device_id'] != 'Null' else 'no asset'}"

    timeline = add_timeline('normalize', details)
    
    incident['timeline'].extend(timeline if isinstance(timeline, list) else [timeline])

    return incident