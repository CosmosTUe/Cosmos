#!/bin/sh
cd Cosmos
git checkout development
git pull
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
systemctl restart cosmos-website.service
