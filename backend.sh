#!/bin/bash

BACKEND_DIR="$HOME/21f1000147/code/backend"
echo "-----Activating Virtual Environment-----"
( source "$BACKEND_DIR/.venv/bin/activate" && echo "-----Completed-----" ) || (echo "-----Environment Activation Failed-----"; exit 1)

python3 "$BACKEND_DIR/main.py"

