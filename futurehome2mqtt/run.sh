#!/usr/bin/with-contenv bashio
set -e

export FIMPSERVER=$(bashio::config 'fimpserver')
export FIMPUSERNAME=$(bashio::config 'fimpusername')
export FIMPPASSWORD=$(bashio::config 'fimppassword')
export FIMPPORT=$(bashio::config 'fimpport')
export CLIENT_ID=$(bashio::config 'client_id')
export DEBUG=$(bashio::config 'debug')
export SELECTED_DEVICES=$(bashio::config 'selected_devices')
export PYTHONUNBUFFERED=1

echo $FIMPSERVER
echo $FIMPUSERNAME
echo $FIMPPORT
echo $CLIENT_ID
echo $DEBUG
echo $SELECTED_DEVICES

echo Starting Futurehome FIMP to Home Assistant
python3 run.py serve
