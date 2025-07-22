#!/bin/bash

echo "Script for running service"
PROJECT_DIR=week1-portfolio-site



echo "Changing directory to project: $PROJECT_DIR"
cd "$PROJECT_DIR"

echo "Feteching latest code form Github..."
git fetch && git reset origin/main --hard

echo "Activating Python Virtual environment"
if [ ! -d venv ]; then
	echo "Creating Virtual environment"
	python3 -m venv venv
fi

source venv/bin/activate

echo "Installing python dependencies"
pip install -r requirements.txt

echo "Restating myportfolio systemd service"

sudo systemctl daemon-reload
sudo systemctl restart myportfolio.service

echo "Deployment done"


