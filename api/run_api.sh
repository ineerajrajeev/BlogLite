#! /bin/sh
echo "======================================================================"
echo "Welcome to blog lite application"
echo "Project for Modern application development-2"
echo "By - Shetkar Neeraj Rajeev (21f1006328)"
echo "This file makes sure if all dependencies are available in virtual environment"
echo "Also make sure if redis is online"
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    virtualenv .env
fi

# Activate virtual env
. .env/bin/activate

# Make sure redis server is running
services redis-server restart

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt

# Now activate the venv and run main.py
