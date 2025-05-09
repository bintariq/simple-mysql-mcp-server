#!/bin/bash

echo "🔧 Installing Simple MySQL MCP Server..."

# Copy config template
if [ -f "config.sample.json" ]; then
  cp config.sample.json config.json
  echo "✅ config.json created from config.sample.json"
else
  echo "❌ config.sample.json not found!"
  exit 1
fi

# Install Python dependencies
if command -v pip &> /dev/null; then
  pip install -r requirements.txt
else
  echo "❌ pip not found. Please install Python and pip first."
  exit 1
fi

echo "✅ Dependencies installed."
echo "🚀 To start the server, run:"
echo "uvicorn main:app --host 0.0.0.0 --port 8081"
