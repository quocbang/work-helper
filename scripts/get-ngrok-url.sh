#!/bin/bash

# Wait for ngrok to start
sleep 20

# Get the public URL
url=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^[:space:]]*\.ngrok-free\.app')

if [ -n "$url" ]; then
    # Only output the URL, no additional messages
    echo "$url"
else
    echo "Failed to get ngrok URL" >&2  # Send error to stderr
    exit 1
fi