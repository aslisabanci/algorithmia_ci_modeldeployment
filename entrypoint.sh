#!/bin/bash

git clone https://"$INPUT_ALGORITHMIA_USERNAME":"$INPUT_ALGORITHMIA_PASSWORD"@git.algorithmia.com/git/"$INPUT_ALGORITHMIA_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git
python3 /entrypoint.py
cd "$INPUT_ALGORITHMIA_ALGONAME"
git config --global user.name "$INPUT_ALGORITHMIA_USERNAME"
git config --global user.email "asabanci+githubCI@algorithmia.io"
git add .
git commit -m "Automated deployment via Github CI"
git push