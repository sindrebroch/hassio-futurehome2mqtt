#!/usr/bin/env bashio
set -e

export FIMPSERVER=$(bashio::config 'fimpserver')
export FIMPUSERNAME=$(bashio::config 'fimpusername')
export FIMPPASSWORD=$(bashio::config 'fimppassword')
export FIMPPORT=$(bashio::config 'fimpport')
export CLIENT_ID=$(bashio::config 'client_id')
export DEBUG=$(bashio::config 'debug')
export SELECTED_DEVICES=$(bashio::config 'selected_devices')
export PYTHONUNBUFFERED=1

export TEST_ENV=os.getenv('fimpport', '1000')

echo "Environment variables:"
env

echo Starting Futurehome FIMP to Home Assistant
python3 run.py serve