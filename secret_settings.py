"""
Contains all the secrets for the website. Production uses a different file, that is not pushed to github.
"""

import json
from os import path

secrets = {
    "SECRET_KEY": "j@7*rtssewjfhix2f^7&1iypigm=o4ju1qtdd!)ad$s1*hlkj2",
    "DEBUG": True,
    "ALLOWED_HOSTS": [],
    "DATABASE_NAME": "cosmos_website_test",
    "DATABASE_USER": "cosmos_website_tester",
    "DATABASE_PASSWORD": "2020123",
    "DATABASE_HOST": "localhost",
    "DATABASE_PORT": "",
    "DATABASE_LEGACY_NAME": "cosmos_website_test_legacy",
    "DATABASE_LEGACY_USER": "cosmos_website_tester_legacy",
    "DATABASE_LEGACY_PASSWORD": "2020123",
    "DATABASE_LEGACY_HOST": "localhost",
    "DATABASE_LEGACY_PORT": "",
    "PRETIX_DOMAIN": "http://localhost:8345",
    # TODO store tokens per team
    "PRETIX_AUTHORIZATION_HEADER": {
        "Authorization": "Token qe7op3k271qtdi1pspbdpxlhcm7oyve4fgkxdrkcucrjmiwdey8bdebcokz4ar8y"
    },
}

if path.exists("/etc/secrets.json"):
    with open("/etc/secrets.json", "r") as f:
        secrets = json.load(f)
