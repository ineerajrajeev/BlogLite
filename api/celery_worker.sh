#! /bin/sh
echo "======================================================================"
echo "Welcome to blog lite application"
echo "Project for Modern application development-2"
echo "By - Shetkar Neeraj Rajeev (21f1006328)"
echo "This file runs celery worker"
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo ".env folder exists. Running celery worker"
else
    echo "creating .env and install using pip"
    virtualenv .env
fi

# Activate virtual env
. .env/bin/activate


celery -A main.celery worker --loglevel=info
