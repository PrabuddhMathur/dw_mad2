from flask import Flask
from application.config import Config, SECRET_KEY
from passlib.hash import pbkdf2_sha256 as passhash
from application.database import db
from application.models import *
from flask_cors import CORS
import secrets
from application import workers


app=None

def create_app():
    app=Flask(__name__)
    CORS(app, origins='http://localhost:5173')
    app.config.from_object(Config)
    app.secret_key=SECRET_KEY
    db.init_app(app)
    app.app_context().push()
    
    db.create_all()

    admin_user = User.query.filter_by(role='admin').first()
    if not admin_user:
        fname='The'
        lname='Admin'
        username = 'admin'
        password = '1234'
        role='admin'
        approved=True

        admin_user=User(fname=fname, lname=lname,username=username,password=passhash.hash(password),role=role,approved=approved)
        status=Visited(user_id=admin_user.id, status=True)
        
        db.session.add(status)
        db.session.add(admin_user)
        db.session.commit()

        token = Token(user_id=admin_user.id, token=secrets.token_urlsafe(32))

        db.session.add(token)
        db.session.commit()

    app.app_context().push()

     # Initialize Celery
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    from application import tasks
    celery.Task = workers.ContextTask

    app.app_context().push()

    return app,celery

app,celery = create_app()

from application.apis import *

if __name__=="__main__":
    app.run(host='0.0.0.0', port=1430)