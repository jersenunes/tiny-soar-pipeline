# type: ignore
import os
import sys
from typing import Dict
from src.ingest import ingest_alert
from src.normalize import normalize_alert
from src.enrich import enrich_alert
from src.triage import triage_alert
from src.respond import respond_alert
from src.output import output_alert


"""
This project was developed to automate cybersecurity operations using SOAR.
Through Python scripts:
- Improve detection and response speed.
- Automate manual and repetitive tasks.
- Provide traceability through logs and timelines.
- Enhances incident response efficiency.
"""


def process_incident(alert_file:str) -> Dict:
    try:
        incident = ingest_alert(alert_file)
        incident = normalize_alert(incident)
        incident = enrich_alert(incident)
        incident = triage_alert(incident)
        incident = respond_alert(incident)
        incident = output_alert(incident)
        return incident

    except Exception as e:
        print(f"Error processing alert: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <alert_file.json>")
        sys.exit(1)

    alert_file = sys.argv[1]

    if not os.path.isfile(alert_file):
        print(f"Alert file {alert_file} does not exist")
        sys.exit(1)
    
    process_incident(alert_file)
    

if __name__ == "__main__":
    main()
