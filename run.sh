#!/bin/bash

# to stop on first error
set -e

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

export FLASK_APP=core/server.py

# reset DB
rm core/store.sqlite3
flask db upgrade -d core/migrations/

# Run required migrations
# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run server
gunicorn -c gunicorn_config.py core.server:app
