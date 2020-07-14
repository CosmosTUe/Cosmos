"""
Contains all the secrets for the website. Production uses a different file, that is not pushed to github.
"""

import json
from os import path

default_secrets = {
    "SECRET_KEY": "j@7*rtssewjfhix2f^7&1iypigm=o4ju1qtdd!)ad$s1*hlkj2",
    "DEBUG": True,
    "ALLOWED_HOSTS": [],
    "DATABASE_NAME": "cosmos_website_test",
    "DATABASE_USER": "cosmos_website_tester",
    "DATABASE_PASSWORD": "2020123",
    "DATABASE_HOST": "localhost",
    "DATABASE_PORT": "",
}


def get_secret(secret):
    if path.exists("/etc/secrets.json"):
        with open("/etc/secrets.json", "r") as f:
            secrets = json.load(f)
            return secrets[secret]
    else:
        return default_secrets[secret]
