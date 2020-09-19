#!/bin/bash

# Install the dependencies of this repo to be able to run the notebook
pip3 install -r requirements.txt

# Clone the Algorithmia algorithm repository
git clone https://"$INPUT_ALGORITHMIA_USERNAME":"$INPUT_ALGORITHMIA_PASSWORD"@git.algorithmia.com/git/"$INPUT_ALGORITHMIA_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git

# Start the action operations to:
#   - (Optionally) run the notebook
#   - Upload the model file to Algorithmia
#   - Link the algorithm with the uploaded model
python3 /entrypoint.py

# Push algorithm updates to Algorithmia
cd "$INPUT_ALGORITHMIA_ALGONAME"
git config --global user.name "$INPUT_ALGORITHMIA_USERNAME"
git config --global user.email "asabanci+githubCI@algorithmia.io"
git add .
git commit -m "Automated deployment via Github CI"
git push