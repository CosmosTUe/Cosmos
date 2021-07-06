"""
Contains all the secrets for the website. Production uses a different file, that is not pushed to github.
"""

import json
import os

if os.path.exists("/etc/secrets.json"):
    with open("/etc/secrets.json", "r") as f:
        secrets = json.load(f)
elif os.path.exists("tests/secrets.json"):
    with open("tests/secrets.json", "r") as f:
        secrets = json.load(f)
else:
    raise FileNotFoundError("secrets.json file not found. Please refer to the Cosmos website wiki.")
