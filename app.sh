#!/bin/bash

function error_exit {
    echo "$1" 1>&2
    exit 1
}

source MAS_env/bin/activate
streamlit run app.py || error_exit "Failed to run Streamlit app."