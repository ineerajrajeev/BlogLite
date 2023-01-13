from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify, make_response, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api, reqparse
from functools import wraps
import uuid
import csv
import jwt
import io
import redis
import random
import string
import json
import smtplib
from werkzeug.utils import secure_filename
import urllib.request
from sqlalchemy.sql import operators, extract
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
from celery.schedules import crontab
from celery.schedules import crontab
import weasyprint


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

SMTP_SERVER_HOST = 'localhost'
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = 'admin@blogLite.co.in'
SENDER_PASSWORD = ''


def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    return True


celery = Celery("Application Jobs")
HOST = 'localhost'
PORT = 6379
celery.conf.update(
    broker_url='redis://{}:{}/{}'.format(HOST, PORT, 0),
    result_backend='redis://{}:{}/{}'.format(HOST, PORT, 0),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    beat_schedule={
        'send-daily-email': {
            'task': 'main.reminder',
            'schedule': crontab(hour=18, minute=0),
        },
        'send_monthly_email': {
            'task': 'main.monthly_report',
            'schedule': crontab(hour=7, minute=0, day_of_month=1),
        }
    }
)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
