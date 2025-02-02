#!/bin/bash

CONFIG_FILE="config/default.yaml"
ENV_FILE=".env"

# Function to update YAML config
update_config() {
    local key=$1
    local value=$2
    sed -i "s/^$key:.*/$key: $value/" "$CONFIG_FILE"
}

# Function to update environment variables
update_env() {
    local key=$1
    local value=$2
    if grep -q "^$key=" "$ENV_FILE"; then
        sed -i "s/^$key=.*/$key=$value/" "$ENV_FILE"
    else
        echo "$key=$value" >> "$ENV_FILE"
    fi
}

# Interactive Configuration
echo "🔧 KQI Platform Configuration Setup"
echo "----------------------------------"

read -p "Enter API Key: " API_KEY
update_env "KQI_API_KEY" "$API_KEY"

read -p "Enter Trading Mode (live/demo): " TRADING_MODE
update_config "trading_mode" "$TRADING_MODE"

read -p "Enter Default Risk Level (0.1 - 1.0): " RISK_LEVEL
update_config "risk_level" "$RISK_LEVEL"

read -p "Enable Auto-Optimization? (yes/no): " AUTO_OPTIMIZE
update_config "auto_optimize" "$AUTO_OPTIMIZE"

read -p "Enter Deployment Environment (dev/prod): " DEPLOY_ENV
update_env "DEPLOY_ENV" "$DEPLOY_ENV"

# Confirm and Save Settings
echo "✅ Configuration updated successfully!"
echo "📂 Config saved to: $CONFIG_FILE"
echo "🔑 Environment variables saved to: $ENV_FILE"