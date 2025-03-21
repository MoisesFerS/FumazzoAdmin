#!/bin/bash

echo "Python versão:"
python --version

echo "Pip versão:"
python -m pip --version

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
