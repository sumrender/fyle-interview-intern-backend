#!/bin/bash

export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/

if [[ "$*" == *"-cov"* ]]; then
    pytest -v --cov-report html:htmlcov --cov-config=.coveragerc --cov=core
else
    pytest -vvv -s tests/
fi