#!/usr/bin/env bash

LAMBDA_LAYER="lambda_layer"
SITE_PACKAGE_PREFIX="/python/lib/python3.11/site-packages"

# Check if the script is called from the right directory
if [[ -d "./dependencies" ]]; then
    echo "Cleaning dependencies directory"
    rm -r dependencies
fi

if [[ -f "./requirements.txt" ]]; then
    echo "File 'requirements.txt' exists in the current directory."
else
    echo "File 'requirements.txt' does not exist in the current directory."
    exit 1  # Exit the script if 'requirements.txt' file does not exist
fi

# Install requirements
pip3 install -t dependencies -r requirements.txt

# Create artifact.zip file
(cd dependencies; zip -r ../lambda_function.zip .)
zip -r lambda_function.zip src
