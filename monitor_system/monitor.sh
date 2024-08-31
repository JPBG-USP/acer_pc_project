#!/bin/bash

if [ "$1" == "server" ]; then
    python3 scripts/server.py
elif [ "$1" == "client" ]; then
    python3 scripts/client.py
else
    echo "Uso: monitor_system {server|client}"
fi
