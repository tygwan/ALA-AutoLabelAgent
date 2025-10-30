#!/bin/bash

# Load NVM environment
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  

# Use Node.js 16
nvm use 16

# Set API keys (replace with your actual keys)
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY_HERE"
export PERPLEXITY_API_KEY="YOUR_PERPLEXITY_API_KEY_HERE"
export OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE"
export GOOGLE_API_KEY="AIzaSyAP-CLweel23OirPckPR7bNgf0nGSowabY"
export MISTRAL_API_KEY="YOUR_MISTRAL_KEY_HERE"
export OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY_HERE"
export XAI_API_KEY="YOUR_XAI_KEY_HERE"
export AZURE_OPENAI_API_KEY="YOUR_AZURE_KEY_HERE"

# Set model configuration
export model="gemini-2.5-pro-exp-05-05"
export MAX_TOKENS="64000"
export TEMPERATURE="0.2"
export DEFAULT_SUBTASKS="5"
export DEFAULT_PRIORITY="medium"
export DEFAULT_MODEL="gemini-2.5-pro-exp-05-05"

# Run Task Master with absolute path to project
npx task-master-ai "$@" 