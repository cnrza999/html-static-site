#!/bin/bash

REPO_NAME="html-static-site"

python3 src/main.py "/${REPO_NAME}/"

echo "Site built successfully with basepath: /${REPO_NAME}/"