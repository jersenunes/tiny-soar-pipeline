# type: ignore
from configs.settings import *
from src.utils import read_a_yaml_file, add_timeline


def severity_by_type(type):
    return {'Phishing': 60, 'Beaconing': 65, 'Malware': 70, 'CredentialAccess': 75}.get(type, 40)


def set_bucket(severity: int) -> str:
    if (severity == 0):
        return 'Suppressed'
    if (severity >= 1 and severity <= 39):
        return 'Low'
    if (severity >= 40 and severity <= 69):
        return 'Medium'
    if (severity >= 70 and severity <= 89):
        return 'High'
    if (severity >= 90 and severity <=100):
        return 'Critical'


def intel_boosts(severity, indicators, allowlisted):
    malicious_score = 0
    suspicious_score = 0 
    allowlist = []
    tags = []
    suppressed = False

    for type, value in allowlisted.items():
        if value:
            allowlist.extend(value if isinstance(value, list) else [value])

    ioc_allowed = [indicator['value'] for indicator in indicators if indicator['value'] in allowlist]
    verdicts_list = [indicator['risk']['verdict'] for indicator in indicators if indicator['value'] not in allowlist]

    if verdicts_list:
        for verdict in verdicts_list:
            if verdict == 'malicious' and malicious_score < 40:
                tags.append('malicious')
                if malicious_score == 0:
                    malicious_score += 20
                else:
                    malicious_score += 5

            elif verdict == 'suspicious' and suspicious_score < 30:
                tags.append('suspicious')
                if suspicious_score == 0:
                    suspicious_score += 10
                else:
                    suspicious_score += 5

    if malicious_score:
        severity += malicious_score
    if suspicious_score:
        severity += suspicious_score

    if ioc_allowed:
        tags.append('allowlisted')
        severity -= (len(ioc_allowed) * 25)

        if not verdicts_list:
            tags.append('suppressed=true')
            suppressed = True
            severity = 0

    if severity < 0:
        severity = 0
    elif severity > 100:
        severity = 100

    bucket = set_bucket(severity)
    tags = list(set(tags))

    return {'severity': severity, 'bucket': bucket, 'tags': tags, 'suppressed': suppressed}


def triage_alert(incident):
    incident_type = incident['source_alert']['type']
    base_severity = severity_by_type(incident['source_alert']['type'])
    
    allow_listed = read_a_yaml_file(ALLOWLISTS)
    
    triage = intel_boosts(base_severity, incident['indicators'], allow_listed['indicators'])

    mitre_map = read_a_yaml_file(MITREMAP)

    mitre = {'techniques': mitre_map['types'].get(incident_type, mitre_map['types'].get('defaults', []))}

    incident.update({'triage': triage, 'mitre': mitre})

    details = f"Severity={triage['severity']} ({triage['bucket']}), tags={triage['tags']}"
    timeline = add_timeline('triage', details)
    
    incident['timeline'].extend(timeline if isinstance(timeline, list) else [timeline])

    return incident