#!/bin/sh
cd /home/prod/Cosmos
git checkout development
git pull
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo systemctl restart cosmos-website.service
