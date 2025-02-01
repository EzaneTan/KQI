#!/bin/bash

# Deploy Agent Script for KQI Platform
# Usage: ./deploy_agent.sh <config_file>

# Check if the configuration file is provided
if [ -z "$1" ]; then
  echo "Error: No configuration file provided."
  echo "Usage: ./deploy_agent.sh <config_file>"
  exit 1
fi

CONFIG_FILE=$1

# Validate the configuration file
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: Configuration file '$CONFIG_FILE' not found."
  exit 1
fi

# Load configuration
echo "Loading configuration from $CONFIG_FILE..."
AGENT_NAME=$(yq e '.agent.name' "$CONFIG_FILE")
STRATEGY=$(yq e '.agent.strategy' "$CONFIG_FILE")
RISK_LEVEL=$(yq e '.agent.risk_level' "$CONFIG_FILE")
PROTOCOLS=$(yq e '.agent.protocols[]' "$CONFIG_FILE" | tr '\n' ', ' | sed 's/, $//')
API_KEY=$(yq e '.api.key' "$CONFIG_FILE")

# Validate required fields
if [ -z "$AGENT_NAME" ] || [ -z "$STRATEGY" ] || [ -z "$API_KEY" ]; then
  echo "Error: Missing required fields in the configuration file."
  exit 1
fi

# Print configuration summary
echo "Agent Name: $AGENT_NAME"
echo "Strategy: $STRATEGY"
echo "Risk Level: $RISK_LEVEL"
echo "Protocols: $PROTOCOLS"
echo "API Key: ********"  # Do not print the actual API key

# Deploy the agent
echo "Deploying agent '$AGENT_NAME' with strategy '$STRATEGY'..."
kqi agent deploy --config "$CONFIG_FILE"

# Check deployment status
if [ $? -eq 0 ]; then
  echo "Agent '$AGENT_NAME' deployed successfully!"
else
  echo "Error: Failed to deploy agent '$AGENT_NAME'."
  exit 1
fi