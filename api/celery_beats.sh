#! /bin/sh
echo "======================================================================"
echo "Welcome to blog lite application"
echo "Project for Modern application development-2"
echo "By - Shetkar Neeraj Rajeev (21f1006328)"
echo "This file runs celery beats"
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo ".env folder exists. Runningcelery beats"
else
    echo "creating .env and install using pip"
    virtualenv .env
fi

# Activate virtual env
. .env/bin/activate


celery -A main.celery beat --loglevel=info
