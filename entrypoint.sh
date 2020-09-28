#!/bin/bash

# Install the dependencies of this repo to be able to run the notebook
pip3 install -r requirements.txt

# Clone the Algorithmia algorithm repository
CI_ALGO_DIR=$INPUT_ALGORITHMIA_ALGONAME"_CI"
git clone https://"$INPUT_ALGORITHMIA_USERNAME":"$INPUT_ALGORITHMIA_PASSWORD"@git.algorithmia.com/git/"$INPUT_ALGORITHMIA_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git $CI_ALGO_DIR

# Run action main to:
#   - (Optionally) run the notebook file
#   - Upload the model file to Algorithmia
#   - Link the algorithm with the uploaded model
python3 /src/action_main.py

# Push updates to Algorithmia, and trigger a new algorithm build
if [ $? -eq 0 ]
then
    echo "Successfully executed action script, optionally executing the model notebook and uploading the model file to Algorithmia.\n"

    if ! [ -e $INPUT_ALGORITHMIA_ALGONAME.py ]
    then
        echo "$INPUT_ALGORITHMIA_ALGONAME.py does not exist. Checking if $INPUT_ALGORITHMIA_ALGONAME.ipynb exists."
        if [ -e $INPUT_ALGORITHMIA_ALGONAME.ipynb ]
        then 
            echo "Found $INPUT_ALGORITHMIA_ALGONAME.ipynb. Will convert this into .py before pushing it to Algorithmia."
        else
            echo "Neither $INPUT_ALGORITHMIA_ALGONAME.ipynb or $INPUT_ALGORITHMIA_ALGONAME.py exist." 
        fi
    fi

    if [ -e $INPUT_ALGORITHMIA_ALGONAME.py ]
    then
        echo "Will copy and push $INPUT_ALGORITHMIA_ALGONAME.py to Algorithm repository."
        cp -R "$INPUT_ALGORITHMIA_ALGONAME.py" $CI_ALGO_DIR/src/
    else
        echo "Will not copy any inference code to Algorithmia."
    fi

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

