#!/bin/bash
chroma run --path data/chromadb &

sleep 5

gunicorn -w 4 -b 0.0.0.0:8080 --timeout 600 scripts.server.app:app


