import json
import os

# Path to the JSON file
ZONE_FILE = os.path.join(os.path.dirname(__file__), 'zones.json')

# Load zones from the JSON file
with open(ZONE_FILE, 'r') as file:
    zones = json.load(file)

# Assign zones to variables
HR_ZONES = zones.get("HR_ZONES", [])
PACE_ZONES = zones.get("PACE_ZONES", [])
CADENCE_ZONES = zones.get("CADENCE_ZONES", [])
BODY_MASS_KG = zones.get("BODY_MASS_KG", None)
HR_REST = zones.get("HR_REST", None)
HR_MAX = zones.get("HR_MAX", None)