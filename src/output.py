import os
from typing import Dict
from pathlib import Path
from configs.settings import *
from src.utils import save_a_json, write_a_file
from jinja2 import Environment, FileSystemLoader


def make_summary(incident: Dict):
    folder_templates = Environment(loader=FileSystemLoader(TEMPLATES))
    template = folder_templates.get_template(SUMMARY_TEMPLATE)

    summary_md = template.render(incident=incident)

    SUMMARIES.mkdir(parents=True, exist_ok=True)
    summary_file = SUMMARIES / f"{incident['incident_id']}.md"
    summary_file.write_text(summary_md, encoding='utf-8')


def output_alert(incident: Dict) -> Dict:
    incident_path = Path(os.path.join(INCIDENTS, f"{incident['incident_id']}.json"))
    
    if incident.get('actions'):
        write_a_file(ISOLATION, incident['actions'])

    save_a_json(incident_path, incident)

    make_summary(incident)

    return incident

    