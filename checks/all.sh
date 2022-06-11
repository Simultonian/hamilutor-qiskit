#!/bin/bash

# ensuring the folder is `checks/`
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ".."

for f in checks/*; 
do
    # skip the present file
    if [ "$f" == "checks/all.sh" ] ; then
        continue;
    fi
    echo "Running $f"
    bash "$f" 
done
