#!/bin/bash
set -e

echo "Packaging backend..."
zip -r deploy.zip app.py requirements.txt -x "*.pyc" -x "__pycache__/*"

echo "Deploying to Azure Web App..."
az webapp deploy \
  --resource-group squash \
  --name squashranking-brhba8aqhbbcfmeq \
  --src-path deploy.zip \
  --type zip

rm deploy.zip
echo "Done. Backend deployed."
