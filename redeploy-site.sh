#!/bin/bash

echo "Script for running service"
PROJECT_DIR=week1-portfolio-site



echo "Changing directory to project: $PROJECT_DIR"
cd "$PROJECT_DIR"

echo "Feteching latest code form Github..."
git fetch && git reset origin/main --hard

echo "Running Docker command"
docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build


echo "Completed !!!"


