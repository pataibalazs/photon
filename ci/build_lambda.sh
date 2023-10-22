#!/usr/bin/env bash

LAMBDA_LAYER="lambda_layer"
SITE_PACKAGE_PREFIX="/python/lib/python3.11/site-packages"

# Check if the script is called from the right directory
if [[ -d "./dependencies" ]]; then
    echo "Recreating dependencies..."
    rm -r dependencies
else
  echo "Creating dependencies..."
fi

if [[ -f "./lambda_function.zip" ]]; then
    rm ./lambda_function.zip
fi

# Install requirements
pip3 install -t dependencies -r requirements.txt

# Create artifact.zip file
(cd dependencies; zip -r ../lambda_function.zip .)
zip -r lambda_function.zip src
