#!/bin/bash

# Set variables
VENV_PATH="../../venv/bin"
FASTAPI_APP="main:app"

# Activate the virtual environment
source "$VENV_PATH/activate"

# Run the FastAPI app using uvicorn
"$VENV_PATH/uvicorn" $FASTAPI_APP --host=0.0.0.0 --port=8000
