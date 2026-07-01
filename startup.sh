#!/usr/bin/env bash
set -e

python -c "from app import setup; setup()"
gunicorn --bind=0.0.0.0 --timeout 600 app:app
