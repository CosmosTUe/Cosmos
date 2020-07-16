#!/bin/sh
cd Cosmos
git checkout master
git pull
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
systemctl restart cosmos-website.service
