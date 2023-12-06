from flask import request
from flask import current_app as app
# from application.models import *
from application.data_access import *

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
