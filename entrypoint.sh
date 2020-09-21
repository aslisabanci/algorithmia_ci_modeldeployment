#!/bin/bash

# Install the dependencies of this repo to be able to run the notebook
pip3 install -r requirements.txt

# Clone the Algorithmia algorithm repository
CI_ALGO_DIR=$INPUT_ALGORITHMIA_ALGONAME"_CI"
git clone https://"$INPUT_ALGORITHMIA_USERNAME":"$INPUT_ALGORITHMIA_PASSWORD"@git.algorithmia.com/git/"$INPUT_ALGORITHMIA_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git $CI_ALGO_DIR
cp -R "$INPUT_ALGORITHMIA_ALGONAME"/. $CI_ALGO_DIR/

# Run action main to:
#   - (Optionally) run the notebook file
#   - Upload the model file to Algorithmia
#   - Link the algorithm with the uploaded model
python3 /src/action_main.py

# Push updates to Algorithmia, and trigger a new algorithm build
if [ $? -eq 0 ]
then
    echo "Successfully executed action script, for optional notebook execution and model file upload.\n Now pushing updates to Algorithmia."
    cd $CI_ALGO_DIR
    git config --global user.name "$INPUT_ALGORITHMIA_USERNAME"
    git config --global user.email "$INPUT_ALGORITHMIA_EMAIL"
    git add .
    git commit -m "Automated deployment via Github CI"
    git push
else
  echo "Action script exited with error." >&2
  exit 1
fi

