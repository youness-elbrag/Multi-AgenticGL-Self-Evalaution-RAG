!curl https://ollama.ai/install.sh | sh

systemctl >/dev/null && sudo systemctl start ollama

!ollama pull llama3