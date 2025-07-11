#!/bin/bash
echo "List all tmux session:"
tmux ls 2>/dev/null || echo "No tmux sessions running"

echo "Killing tmux session..."
tmux ls 2>/dev/null | cut -d: -f1 | xargs -r -n1 tmux kill-session -t


echo "Changing to the actual project folder"
PROJECT_DIR=week1-portfolio-site
SESSION_NAME=week1


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

echo "Starting new detached tmux session: $SESSION_NAME"
tmux new-session -d -s "$SESSION_NAME"
tmux send-keys -t "$SESSION_NAME" "cd $PROJECT_DIR" C-m
tmux send-keys -t "$SESSION_NAME" "source venv/bin/activate" C-m
tmux send-keys -t "$SESSION_NAME" "flask run --host=0.0.0.0 --port=5000" C-m


