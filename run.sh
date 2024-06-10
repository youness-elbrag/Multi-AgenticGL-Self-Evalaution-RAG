#!/bin/bash

function error_exit {
    echo "$1" 1>&2
    exit 1
}

virtualenv -p $(which python3.12) MAS_env || error_exit "Failed to create virtual environment."

clear

source MAS_env/bin/activate || error_exit "Failed to activate virtual environment."

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || error_exit "Failed to install dependencies."
else
    error_exit "requirements.txt not found. Please make sure it is in the same directory as this script."
fi

clear

