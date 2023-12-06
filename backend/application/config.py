import os
basedir=os.path.abspath(os.path.dirname(__file__))

SECRET_KEY="kamsamnida"

class Config():
    SQLITE_DB_DIR=os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(SQLITE_DB_DIR, "dbase.db")
    DEBUG=True
    CACHE_TYPE= 'redis'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_DEFAULT_TIMEOUT= 300
    # CELERY_BROKER_URL = "redis://localhost:6379/1"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379/2"