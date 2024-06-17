#!/bin/bash

if ! command -v curl &> /dev/null
then
    echo "curl could not be found. Please install curl and try again."
    exit 1
fi

# Install Ollama
echo "Installing Ollama..."
curl -s https://ollama.ai/install.sh | sh

# Start Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

export OLLAMA_HOST="127.0.0.1:11434"
echo "Environment variable OLLAMA_HOST set to $OLLAMA_HOST"

echo "Pulling Llama3 model..."
ollama pull llama3

echo "Verifying Ollama installation..."
ollama -v
echo "Setup completed successfully."


