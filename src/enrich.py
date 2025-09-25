# type: ignore
import os
from configs.settings import *
from src.utils import read_a_json_file, read_a_yaml_file, get_files, add_timeline
from typing import Dict


def return_total_risks(risks:Dict, type:str) -> int:
    risk_list = [risk['risk']['verdict'] for risk in risks if risk['risk']['verdict'] == type]
    return len(risk_list)


def get_provider_path(provider_name: str, yaml_file: dict) -> str:
    base_url = yaml_file['providers'][provider_name]['base_url']

    if base_url.startswith('file://'):
        base_path = ROOT_FOLDER / base_url.replace('file://', '')
    else:
        base_path = ROOT_FOLDER / base_url

    filename = get_files(base_path, provider_name)

    return os.path.join(base_path, f'{filename}')


def get_verdict(verdict_value:Dict) -> Dict:
    if verdict_value.get('risk'):
        verdict = verdict_value.get('risk')
    elif verdict_value.get('reputation'):
        verdict = verdict_value.get('reputation')
    elif verdict_value.get('classification'):
        verdict = verdict_value.get('classification')
    else:
        verdict = 'unknown'


    score = verdict_value.get('confidence') or verdict_value.get('score') or 0

    
    return {'verdict':verdict, 'score': score}


def get_risk(current_risk:Dict, indicator:Dict) -> Dict:
    new_risk = get_verdict(indicator)
    if not current_risk or new_risk['score'] > current_risk.get('score', 0):
        return new_risk
    return current_risk


def enrich_alert(incident:Dict) -> Dict:
    """
    The enrich module enhances the ingested data using local threat intelligence sources.
    Adds context and severity levels for better prioritization.
    For each indicator, the module selects the highest score available.
    The enriched indicators are added back into the incident, along with updated timeline details.  
    """

    indicators_list = []
    providers_verdicts = {}
    
    path_connectors = read_a_yaml_file(CONNECTORS)

    for provider in PROVIDER_NAMES:
        provider_path = get_provider_path(provider, path_connectors)
        providers_verdicts.update({provider:read_a_json_file(provider_path)})

    for indicator in incident['indicators']:
        risk = {}
        sources = []
        for key, value in providers_verdicts.items():
            if indicator['value'] in value.get('ip', []):
                sources.append(key)
                risk.update(get_risk(risk, value))

            elif indicator['value'] in value.get('domain', []):
                sources.append(key)
                risk.update(get_risk(risk, value))

            elif indicator['value'] in value.get('url', []):
                sources.append(key)
                risk.update(get_risk(risk, value))

            elif indicator['value'] in value.get('sha256', []):
                sources.append(key)
                risk.update(get_risk(risk, value))
        if not risk:
            risk.update(get_risk(risk, {}))
        
        risk.update({'sources': sources})        
        indicator.update({'risk': risk, 'allowlisted': False})

        indicators_list.append(indicator)

    incident['indicators'] = indicators_list

    risk_malicious = return_total_risks(indicators_list, 'malicious')
    risk_suspicious = return_total_risks(indicators_list, 'suspicious')
    risk_clean = return_total_risks(indicators_list, 'clean')
    risk_unknown = return_total_risks(indicators_list, 'unknown')

    risk_total = risk_malicious + risk_suspicious + risk_clean + risk_unknown

    string_text = ''
    if risk_malicious:
        string_text += f"{risk_malicious} malicious, "
    if risk_suspicious:
        string_text += f"{risk_suspicious} suspicious, "
    if risk_clean:
        string_text += f"{risk_clean} clean, "
    if risk_unknown:
        string_text += f"{risk_unknown} unknown"

    details = f"{risk_total} IOCs enriched: {string_text}"

    timeline = add_timeline('enrich', details)
    
    incident['timeline'].extend(timeline if isinstance(timeline, list) else [timeline])

    return incident

