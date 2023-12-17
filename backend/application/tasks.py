from application.workers import celery
from celery.schedules import crontab
from flask import render_template
from jinja2 import Template
from application.data_access import *
from application.models import *
from application.utils import *
import csv

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month='1', hour=7, minute=30), 
        # 10.0,
        monthly_report.s(), 
        name='Monthly Analytics Report'
    )
    sender.add_periodic_task(
        crontab(hour=7),
        # 10.0,
        send_daily_reminders.s(),
        name="Daily Reminder"
    )

@celery.task()
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

@celery.task()
def send_daily_reminders():
    template_str = """
        <p>
            Hey {{ username }}!
        </p>
        <br />
        <p>
           We are missing you! It looks like you haven't visited in a while. Login to freshness only on Grocilla.
        </p>
        <br />
        <p>
            Looking forward to seeing you there,
        </p>
        <p>
            Grocilla
        </p>
        """
    users=Visited.query.all()
    for user in users:
        the_user=get_user_by_id(user.user_id)
        if the_user.role!="admin" and the_user.role!="manager":
            if not user.status:
                template = Template(template_str)
                address = the_user.username+'@user.com'
                subject = f"Daily Reminder: Hey {the_user.username}! Check out our daily hits!"
                message = template.render(username=the_user.username)

                send_email(address,subject,message)
            user.status=False
            db.session.commit()

@celery.task()
def sendManagerConformation(username):
    template_str = """
        <p>
            Hey {{ username }}!
        </p>
        <br />
        <p>
            Your registeration has been approved. Welcome to Grocilla!
        </p>
        <br />
        <p>
            Looking forward to working with you,
        </p>
        <p>
            Grocilla
        </p>
        """
    template = Template(template_str)
    address = username+'@manager.com'
    subject = f"Registration approved for {username}!"
    message = template.render(username=username)
    send_email(address,subject,message)

@celery.task()
def export_category_csv(cid,manager_id):
    the_category=get_category_by_id(cid)
    the_products=Product.query.filter_by(category_id=cid).all()
    user=get_user_by_id(manager_id)

    with open("category_analytics.csv", "w", newline='') as f:
        f = csv.writer(f, delimiter=',')
        f.writerow(["Category ID","Category Name"])
        f.writerow([the_category.cid,the_category.cname])
        f.writerow(["Product ID","Product Name","Manufacturing Date","Expiry Date","Unit","Rate","Quantity"])
        for product in the_products:
            f.writerow([product.pid,product.pname,product.manf_date,product.exp_date,product.unit,product.rateperunit,product.quantity])

    template_str = """
        <p>
            Dear {{username}},
        </p>
        <br />
        <p>
            As requested, we have attached CSV report for {{ cname }} in this email.
        </p>
        <p>
            If you have any questions or concerns about the report, please don\'t hesitate to reach out to us.
        </p>
        <br />
        <p>
            Best regards,
        </p>
        <p>
            Grocilla
        </p>
        """
    template = Template(template_str)

    address = user.username+'@user.com'
    subject = f"{the_category.cname} details CSV Export"
    message = template.render(username=user.username,cname=the_category.cname)

    file = open("category_analytics.csv", "rb")

    send_email(address, subject, message, attachment=file, filename="category_analytics.csv", subtype="csv")

    os.remove("category_analytics.csv")