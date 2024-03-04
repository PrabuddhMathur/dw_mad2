#!/bin/bash
cd "$HOME/21f1000147/code/backend"
celery -A main.celery worker -l info -E

