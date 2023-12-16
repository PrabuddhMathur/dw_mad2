from application.workers import celery
from celery.schedules import crontab
from flask import render_template
from flask import current_app as app
from jinja2 import Template
from application.data_access import *
from application.models import *
from application.utils import *
import csv

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0,hello.s(),name='testing hello world')
    # sender.add_periodic_task(
    #     # crontab(day_of_month='1', hour=7, minute=30), 
    #     30.0,
    #     monthly_report.s(), 
    #     name='Monthly Analytics Report'
    # )
    # sender.add_periodic_task(
    #     crontab(hour=7),

        # send_daily_reminders.s(),
        # name="Daily Reminder"
    # )

@celery.task
def hello():
    print('hallo dich')

@celery.task
def monthly_report():
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "support@grocilla.com"
    SENDER_PASSWORD = ""
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = "admin@grocilla.com"
    msg["Subject"] = "Admin Monthly Report"
    template = render_template("monthly_report.html")
    msg.attach(MIMEText(template, "html"))

    images=['graph.png']
    for image in images:
        with open("static/" + image, "rb") as fp:
            img = MIMEImage(fp.read(), _subtype='png')
        img.add_header('Content-ID', '<{}>'.format(image))
        msg.attach(img)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()