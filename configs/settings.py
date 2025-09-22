from pathlib import Path

#Set names
PROVIDER_NAMES = ['defender_ti', 'reversinglabs', 'anomali']
SUMMARY_TEMPLATE = 'summary.md.j2'

#Set paths
ROOT_FOLDER = Path(__file__).parent.parent
ALLOWLISTS = ROOT_FOLDER / 'configs' / 'allowlists.yml'
CONNECTORS = ROOT_FOLDER / 'configs' / 'connectors.yml'
MITREMAP = ROOT_FOLDER / 'configs' / 'mitre_map.yml'
INCIDENTS = ROOT_FOLDER / 'out' / 'incidents'
SUMMARIES = ROOT_FOLDER / 'out' / 'summaries'
ISOLATION = ROOT_FOLDER / 'out' / 'isolation.log'
TEMPLATES = ROOT_FOLDER / 'templates'