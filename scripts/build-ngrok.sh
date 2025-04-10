#!/bin/bash

# Kill existing ngrok processes
pkill ngrok

# Start ngrok
ngrok http 5678 --log=stderr > /dev/null 2>&1 &

# Wait a moment
sleep 2

echo "Ngrok is running in background. You can check the URL at http://localhost:4040"
