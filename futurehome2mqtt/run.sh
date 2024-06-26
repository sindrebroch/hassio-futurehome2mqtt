#!/usr/bin/with-contenv bashio
set -e

export FIMPSERVER=$(bashio::config 'fimpserver')
export FIMPUSERNAME=$(bashio::config 'fimpusername')
export FIMPPASSWORD=$(bashio::config 'fimppassword')
export FIMPPORT=$(bashio::config 'fimpport')
export CLIENT_ID=$(bashio::config 'client_id')
export DEBUG=$(bashio::config 'debug')
export PYTHONUNBUFFERED=1

#if [ "$FIMPSERVER" == "null" ]; then
#    source .env;
#fi

echo Starting Futurehome FIMP to Home Assistant
python3 run.py serve
