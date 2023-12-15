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
    else:
        data = request.get_json()
        cname = data["cname"]
        new_category=Category(cname=cname)
        db.session.add(new_category)
        db.session.commit()
        cache.clear()
        return f"Addition of {new_category.cname} successful!"

@app.route("/api/products", methods = ["GET", "POST"])
def getProducts():
    if request.method == "GET":
        products=get_all_products()
        return [product.to_dict() for product in products]

@app.route("/admin-api/category/<int:cid>", methods = ["POST", "DELETE"])
def getCategory(cid):
    new_category=get_category_by_id(cid)
    if request.method=="POST":
        data = request.get_json()
        new_cname=data["cname"]
        new_category.cname=new_cname
        db.session.commit()
        cache.clear()
        return f"Updation for {new_category.cname} successful!"
    else:
        db.session.delete(get_category_by_id(cid))
        db.session.commit()
        cache.clear()
        return "Deletion successful!"

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
        if not user:
            return {"Error" : 404,"message":"Username does not exist"}
        
        if not passhash.verify(password,user.password):
            return {"Error" : 401, "message": "Invalid Password"}
    
        if user.approved:
            token = get_token_by_user_id(user.id)
            encoded = jwt.encode({"token": token}, app.secret_key)
            expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            get_status(user.id).status=True
            db.session.commit()
        
            return {"token": encoded, "expiry": expiry_time}
        else:
            return {"Error":404,"message":"Admin has not approved your account yet. Please try again later."}

@app.route("/api/role")
def role():
    token=request.headers.get("Authorization", "").split(" ")[-1]
    decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
    user_id=get_user_id_by_token(decodedToken['token'])
    role=get_user_by_id(user_id).role
    return {"role":role}
       
@app.route("/admin-api/approval/users")
def user_approvals():
    users=get_user_approval(False)
    return users

@app.route("/admin-api/approval/categories")
def categories_approval():
    updated_categories=get_category_approval()        
    return updated_categories

@app.route("/admin-api/approval/user/<int:user_id>", methods=["GET","DELETE"])
def userid_approved(user_id):
    if request.method=="GET":

        user=get_user_by_id(user_id)
        user.approved=True
        db.session.commit()
        cache.clear()

        return f'Manager {user.username} request approved!'
    else:

        user=get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        cache.clear()
        return f'Manager {user.username} request deleted!'
    
@app.route("/admin-api/approval/category/<int:approval_id>",methods=["GET","DELETE"])
def approvalid_approved(approval_id):
    category=get_category_approval_by_id(approval_id)
    if request.method=="GET":
        if category.request_type=="Add":
            new_category=Category(cname=category.cname)
            db.session.add(new_category)
            db.session.delete(category)
            db.session.commit()
            cache.clear()
            return f"Addition request for {category.cname} category approved!"
        elif category.request_type=="Update":
            updated_category=get_category_by_id(cid=category.category_id)
            updated_category.cname = category.cname
            db.session.delete(category)
            db.session.commit()
            cache.clear()
            return f"Updation request for {category.cname} category approved!"
        elif category.request_type=="Delete":
            db.session.delete(get_category_by_id(category.category_id))
            db.session.delete(category)
            db.session.commit()
            cache.clear()
            return f"Deletion request for {category.cname} category approved!"
    else:
        db.session.delete(category)
        db.session.commit()
        return "Request declined!"

@app.route("/manager-api/approval/category",methods=["POST"])
def manager_category():
    if request.method=="POST":
        data = request.get_json()
        request_type=data["request_type"]
        cname=data["cname"]

        if request_type=="Add":
            add_request=ApproveCategory(request_type=request_type, cname=cname)
            db.session.add(add_request)
            db.session.commit()
            return "Add category request sent!"
        
        elif request_type=="Update":
            cid=data["cid"]
            updated_cname=data["updated_cname"]
            edit_request=ApproveCategory(category_id=cid,request_type=request_type, updated_cname=updated_cname,cname=cname)
            db.session.add(edit_request)
            db.session.commit()
            return "Edit category request sent!"
        
        elif request_type=="Delete":
            cid=data["cid"]
            delete_request=ApproveCategory(category_id=cid,request_type=request_type,cname=cname)
            db.session.add(delete_request)
            db.session.commit()
            return "Delete category request sent!"

#Add product in this API.
@app.route("/manager-api/product/add",methods=["POST"])
def product_add():
    data = request.get_json()
    category_id = data["category_id"]
    pname = data["pname"]
    manf_date = datetime.datetime.strptime(data["manf_date"], '%Y-%m-%d')
    exp_date = datetime.datetime.strptime(data["exp_date"], '%Y-%m-%d')
    unit = data["unit"]
    rateperunit = data["rateperunit"]
    quantity = data["quantity"]
    new_product=Product(category_id=category_id, pname=pname, manf_date=manf_date, exp_date=exp_date, unit=unit, rateperunit=rateperunit, quantity=quantity)
    db.session.add(new_product)
    db.session.commit()
    cache.clear()
    return f"Addition of {new_product.cname} successful!"

#Update and Delete product in this one.
@app.route("/manager-api/product/<int:pid>",methods=["POST","DELETE"])
def product_op(pid):
    new_product=get_product_by_id(pid)
    if request.method=="POST":
        data = request.get_json()
        new_product.pname=data["pname"]
        new_product.manf_date=datetime.datetime.strptime(data["manf_date"], '%Y-%m-%d')
        new_product.exp_date=datetime.datetime.strptime(data["exp_date"], '%Y-%m-%d')
        new_product.unit=data["unit"]
        new_product.rateperunit=data["rateperunit"]
        new_product.quantity=data["quantity"]
        db.session.commit()
        cache.clear()
        return f"Updation for {new_product.pname} successful!"
    else:
        db.session.delete(get_product_by_id(pid))
        db.session.commit()
        cache.clear()
        return "Deletion successful!"

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
