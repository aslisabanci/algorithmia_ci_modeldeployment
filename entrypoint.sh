#!/bin/bash

# `$*` expands the `args` supplied in an `array` individually 
# or splits `args` in a string separated by whitespace.
pwd
ls
git clone https://"$ALGORITHMIA_USERNAME":"$ALGORITHMIA_PASSWORD"@git.algorithmia.com/git/"$ALGORITHMIA_USERNAME"/"$ALGORITHMIA_ALGONAME".git
python3 /entrypoint.py
cd "$ALGORITHMIA_ALGONAME"
git config --global user.name ${{ env.ALGORITHMIA_USERNAME }}
git config --global user.email "asabanci+githubCI@algorithmia.io"
git add .
git commit -m "Automated deployment via Github CI"
git push