#! /bin/env bash

if (!(Test-Path -Path ./env)) {
    python -m venv env
}

env\Scripts\Activate.ps1

pip install -r .\requirements.txt

python main.py

exit 0