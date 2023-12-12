from flask import request
from flask import current_app as app
from application.data_access import *
from passlib.hash import pbkdf2_sha256 as passhash
from application.cache import cache
import jwt, secrets,datetime

@app.route("/api/categories", methods = ["GET", "POST"])
def getCategories():
    if request.method == "GET":
        categories=get_all_categories()
        return categories

@app.route("/api/products", methods = ["GET", "POST"])
def getProducts():
    if request.method == "GET":
        products=get_all_products()
        return [product.to_dict() for product in products]

@app.route("/api/register", methods = ["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        fname = data["fname"]
        lname = data["lname"]
        username = data["username"]
        password = data["password"]
        role = data["role"]

        if get_user_by_username(username):
            return {"Error" : 401, "message":"Username already exists"}
        
        if role == "user":
            approved=True
        else:
            approved=False

        user = User(fname=fname, lname=lname,username=username,password=passhash.hash(password),role=role,approved=approved)
        db.session.add(user)
        db.session.commit()

        token = Token(user_id=user.id, token=secrets.token_urlsafe(32))

        db.session.add(token)
        db.session.commit()

        visit=Visited(user_id=user.id, status=True)
        db.session.add(visit)
        db.session.commit()

        cache.clear()

        token=token.token
        encoded = jwt.encode({"token": token}, app.secret_key)
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        return {"token": encoded, "expiry": expiry_time}

@app.route("/api/login", methods = ["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        user = get_user_by_username(username)
        # print(user)
        if not user:
            return {"Error" : 404,"message":"Username does not exist"}
        
        if passhash.verify(password, user.password):
            token = get_token_by_user_id(user.id)
            encoded = jwt.encode({"token": token}, app.secret_key)
            expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            get_status(user.id).status=True
            db.session.commit()
            return {"token": encoded, "expiry": expiry_time}
        else:
            return {"Error":404,"message":"Incorrect password"}



# @app.route("/api/bookings", methods = ["GET", "POST"])
# def getBookings():
#     if request.method == "GET":
#         bookings = Booking.query.all()
#         return [booking.to_dict() for booking in bookings]

# @app.route("/api/orders", methods = ["GET", "POST"])
# def getOrders():
#     if request.method == "GET":
#         orders = Order.query.all()
#         return [order.to_dict() for order in orders]
