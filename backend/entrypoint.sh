#!/bin/bash

cd /app

if [ ! -d "app/services/contract_build" ]; then
  echo "🛠  No contract_build found — deploying contracts..."
  python3 -m app.services.contractsManager.contract_utils
else
  echo "✅  contract_build already exists — skipping deployment."
fi

echo "🚀 Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
