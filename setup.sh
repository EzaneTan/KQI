#!/bin/bash

# KQI Platform Setup Script
# This script installs dependencies and sets up the environment for KQI.

# Exit on error
set -e

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log messages
log() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

# Function to log errors
error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
  exit 1
}

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  error "Please run this script as root."
fi

# Update and install dependencies
log "Updating package lists..."
apt-get update -qq

log "Installing system dependencies..."
apt-get install -y -qq \
  python3 \
  python3-pip \
  git \
  curl \
  jq \
  yq

# Install Python dependencies
log "Installing Python dependencies..."
pip3 install -q \
  numpy \
  pandas \
  scikit-learn \
  pyyaml

# Install KQI CLI (example, replace with actual installation command)
log "Installing KQI CLI..."
if ! command -v kqi &> /dev/null; then
  curl -sSL https://kqi.ai/install.sh | bash
else
  log "KQI CLI is already installed."
fi

# Clone the KQI repository (if not already cloned)