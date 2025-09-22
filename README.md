# Tiny SOAR Pipeline

This project implements a minimal SOAR pipeline for alert ingestion, normalization, enrichment, triage, response, and output. It simulates response actions (like device isolation) using local mock Threat Intelligence data and generates normalized incidents and Markdown summaries.

---

## Project Structure

```
project/
│
├── src/                     # Source code
│   ├── ingest.py
│   ├── normalize.py
│   ├── enrich.py
│   ├── triage.py
│   ├── respond.py
│   ├── output.py
│   └── utils.py
│
├── tests/                   # Unit tests
├── alerts/                  # Example alert JSONs
├── templates/               # Jinja2 templates for Markdown summaries
├── configs/                 # YAML configs: allowlists, MITRE mapping, connectors
└── out/                     # Output: incident JSONs, logs, and summaries
```

---

## Prerequisites

* Python 3.10+
* Python packages:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
pyyaml
jinja2
pytest
```

---

## Setup

1. Configure **allowlists, MITRE mapping, and connectors** in the `configs/` folder.
2. Place **mock TI JSON files** in the folder paths defined in connectors.
3. Place **example alert JSONs** in `alerts/` for testing.

---

## Running the Pipeline

Via CLI:

```bash
python main.py alerts/sentinel.json
```

The pipeline performs the following steps:

1. **Ingestion**: reads the alert JSON file.
2. **Normalization**: converts source-specific fields into a standardized internal structure.
3. **Enrichment**: adds risk information for IOCs using local mock TI data.
4. **Triage**: calculates severity, bucket, tags, and MITRE techniques.
5. **Response**: simulates device isolation (writes to log only).
6. **Output**: generates incident JSON and Markdown analyst summary.

---

## Output

* `out/incidents/<incident_id>.json` → normalized incident JSON.
* `out/summaries/<incident_id>.md` → analyst Markdown summary.
* `out/isolation.log` → isolation actions log (if applicable).

---

## Unit Testing

The project uses **pytest** for unit testing.

### Run all tests

```bash
pytest -v
```

### Run tests for a specific module

```bash
pytest tests/test_ingest.py
```

### Run a specific test function

```bash
pytest tests/test_ingest.py::test_ingest_alert
```

**Notes:**

* Timeline and actions are validated in all modules.

---

## Notes

* The pipeline runs **offline**, using only local mock TI data.
* It **simulates responses**, without executing real commands on devices.
* The project is modular and can be extended for real connectors, automation, and alerts.

---

## Author

Jersé Nunes
