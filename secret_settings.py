"""
Contains all the secrets for the website. Production uses a different file, that is not pushed to github.
"""

import json
import os
import sys

if sys.platform.startswith(("linux", "darwin")):
    if os.path.exists("/etc/secrets.json"):  # Linux/macOS local dev or staging/production server
        with open("/etc/secrets.json", "r") as f:
            secrets = json.load(f)
    elif os.path.exists("tests/secrets.json"):  # CI server
        with open("tests/secrets.json", "r") as f:
            secrets = json.load(f)
    else:
        raise FileNotFoundError("secrets.json file not found. Please refer to the Cosmos website wiki.")
elif sys.platform.startswith("win32"):
    if os.path.exists(str(os.path.expanduser("~")) + "\\secrets.json"):  # Windows local dev
        with open(str(os.path.expanduser("~")) + "\\secrets.json", "r") as f:
            secrets = json.load(f)
    else:
        raise FileNotFoundError("secrets.json file not found. Please refer to the Cosmos website wiki.")
else:
    raise Exception("Platform not supported")
