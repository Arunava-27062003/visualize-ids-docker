#!/bin/bash

# Start Prometheus in the background
which prometheus
prometheus --config.file=/etc/prometheus/prometheus.yml &

# Start the IDS script
python3 /app/ids_script.py
