#!/bin/sh

echo Starting Server.
exec gunicorn src.app:app -b 0.0.0.0:8000 -w 2 -k uvicorn.workers.UvicornWorker --worker-connections 1000 --max-requests 1000 --worker-tmp-dir /dev/shm
