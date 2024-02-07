#!/bin/bash

cd "$(dirname "$0")"

pytest test_main.py
pytest test_db.py
pytest test_algorithm.py

exit $?
