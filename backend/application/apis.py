from flask import request
from flask import current_app as app
from application.data_access import *
from passlib.hash import pbkdf2_sha256 as passhash
from application.cache import cache
import jwt, secrets,datetime
from application import tasks

@app.route("/api/categories", methods = ["GET", "POST"])
def getCategories():
    if request.method == "GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            categories=get_all_categories()
            return categories
        else:
            return "User not authorized"
        
    elif request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            print(user_id)
            if get_user_by_id(user_id).role=="admin":
                data = request.get_json()
                cname = data["cname"]
                new_category=Category(cname=cname)
                db.session.add(new_category)
                db.session.commit()
                cache.clear()
                return f"Addition of {new_category.cname} successful!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/admin-api/category/<int:cid>", methods = ["POST", "DELETE"])
def getCategory(cid):
    new_category=get_category_by_id(cid)
    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                data = request.get_json()
                new_cname=data["cname"]
                new_category.cname=new_cname
                db.session.commit()
                cache.clear()
                return f"Updation for {new_category.cname} successful!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
        
    elif request.method=="DELETE":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                db.session.delete(new_category)
                db.session.commit()
                cache.clear()
                return "Deletion successful!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

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

@app.route("/api/username")
def username():
    token=request.headers.get("Authorization", "").split(" ")[-1]
    decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
    user_id=get_user_id_by_token(decodedToken['token'])
    fname=User.query.filter_by(id=user_id).first().fname
    lname=User.query.filter_by(id=user_id).first().lname
    username=fname+" "+lname
    return {"username":username}

@app.route("/admin-api/approval/users")
def user_approvals():
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                users=get_user_approval(False)
                return users
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/admin-api/approval/categories")
def categories_approval():
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                updated_categories=ApproveCategory.query.all()       
                return [i.to_dict() for i in updated_categories]
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/manager-api/approval/categories")
def categories_approval_request():
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="manager":
                updated_categories=ApproveCategory.query.filter_by(manager_id=user_id).all()       
                return [i.to_dict() for i in updated_categories]
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/admin-api/approval/user/<int:uid>", methods=["GET","DELETE"])
def userid_approved(uid):
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                user=get_user_by_id(uid)
                user.approved=True
                db.session.commit()
                tasks.sendManagerConformation.delay(user.username)
                cache.clear()

                return f'Manager {user.username} request approved!'
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    elif request.method=="DELETE":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                user=get_user_by_id(user_id)
                db.session.delete(user)
                db.session.commit()
                cache.clear()
                return f'Manager {user.username} request deleted!'
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"
    
@app.route("/admin-api/approval/category/<int:approval_id>",methods=["GET","DELETE"])
def approvalid_approved(approval_id):
    category=ApproveCategory.query.filter_by(id=approval_id).first()
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                if category.request_type=="Add":
                    new_category=Category(cname=category.cname)
                    db.session.add(new_category)
                    db.session.delete(category)
                    db.session.commit()
                    cache.clear()
                    return f"Addition request for {category.cname} category approved!"
                elif category.request_type=="Update":
                    updated_category=get_category_by_id(category.category_id)
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
                return "User operation not allowed"
        else:
            return "User not authorized"
    
    elif request.method=="DELETE":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="admin":
                db.session.delete(category)
                db.session.commit()
                return "Request declined!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/manager-api/approval/category",methods=["POST"])
def manager_category():
    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="manager":
                data = request.get_json()
                request_type=data["request_type"]

                if request_type=="Add":
                    cname=data["cname"]
                    add_request=ApproveCategory(request_type=request_type, cname=cname,manager_id=user_id)
                    db.session.add(add_request)
                    db.session.commit()
                    return "Add category request sent!"
                
                elif request_type=="Update":
                    cid=data["cid"]
                    updated_cname=data["updated_cname"]
                    cname=data["cname"]
                    edit_request=ApproveCategory(category_id=cid,request_type=request_type, updated_cname=updated_cname,cname=cname,manager_id=user_id)
                    db.session.add(edit_request)
                    db.session.commit()
                    return "Edit category request sent!"
                
                elif request_type=="Delete":
                    cid=data["cid"]
                    cat=get_category_by_id(cid)
                    delete_request=ApproveCategory(category_id=cid,request_type=request_type,cname=cat.cname,manager_id=user_id)
                    db.session.add(delete_request)
                    db.session.commit()
                    return "Delete category request sent!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

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

@app.route("/user-api/bookings")
def getBookings():
    if request.method == "GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])

            return get_user_bookings(user_id)
    else:
        return "Invalid HTTP Request"
    
@app.route("/user-api/bookings/<int:pid>",methods=["POST"])
def addBookings(pid):
    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])

            data=request.get_json()
            quantity=data['quantity']
            pid=data['pid']
            product_name=data['product_name']
            category_name=data['category_name']
            
            new_booking=Booking(category_name=category_name,quantity_of_item=quantity,user_id=user_id,item_name=product_name,product_id=pid)
            db.session.add(new_booking)
            db.session.commit()
            cache.clear()
            return "Booking Successful!"
        else: 
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/user-api/bookings/<int:bookingid>",methods=["GET","DELETE"])
def cartActions(bookingid):
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="user":
                booking = get_booking_by_id(bookingid)
                product = get_product_by_id(booking.product_id)
                product_unit = product.unit
                rate = product.rateperunit
                quantity = booking.quantity_of_item
                new_quantity = product.quantity - int(quantity)
                if new_quantity>=0:
                    product.quantity = new_quantity
                    totalprice = int(quantity)*int(rate)
                    order = Order(userid=user_id, productid=product.pid, quantity_of_product=quantity, totalprice=totalprice, product_unit=product_unit, product_name=product.pname)
                    db.session.add(order)
                    db.session.delete(booking)
                    db.session.commit()
                    cache.clear()
                    return "Product successfully purchased!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
        
    elif request.method=="DELETE":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            db.session.delete(get_booking_by_id(bookingid))
            db.session.commit()
            cache.clear()
            return "Booking deletion successful"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"
        
@app.route("/user-api/orders")
def getOrders():
    if request.method == "GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="user":
                orders = get_orders_by_user_id(user_id)
                return orders
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/user-api/bookings/buyall",methods=["GET"])
def buyAll():
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])
            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="user":
                bookings = Booking.query.filter_by(user_id=user_id).all()
                for booking in bookings:
                    product = get_product_by_id(booking.product_id)
                    product_unit = product.unit
                    rate = product.rateperunit
                    quantity = booking.quantity_of_item
                    new_quantity = product.quantity - int(quantity)
                    if new_quantity>=0:
                        product.quantity = new_quantity
                        totalprice = int(quantity)*int(rate)
                        order = Order(userid=user_id, productid=product.pid, totalprice=totalprice, quantity_of_product=quantity, product_unit=product_unit, product_name=product.pname)
                        db.session.add(order)
                        db.session.delete(booking)
                db.session.commit()
                cache.clear()
                return "Products successfully purchased!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/api/products", methods = ["GET"])
def getProducts():
    if request.method == "GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            products=Product.query.all()
            return [i.to_dict() for i in products]
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"
    
@app.route("/user-api/search/category", methods = ["POST"])
def search_categories():
    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            data=request.get_json()
            cat_name = data["category"]
            categories = Category.query.filter(Category.cname.ilike(f"%{cat_name}%"))
            return [i.to_dict() for i in categories]
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"
    
@app.route("/user-api/search/product", methods = ["POST"])
def search_products():
    if request.method=="POST":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            data=request.get_json()
            product_name = data["product"]
            products = Product.query.filter(Product.pname.ilike(f"%{product_name}%"))
            return [i.to_dict() for i in products]
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"

@app.route("/manager-api/analytics/category/<int:cid>", methods = ["GET"])
def export_category(cid):
    if request.method=="GET":
        token=request.headers.get("Authorization", "").split(" ")[-1]
        if token:
            decodedToken=jwt.decode(token,app.secret_key,algorithms=["HS256"])

            user_id=get_user_id_by_token(decodedToken['token'])
            if get_user_by_id(user_id).role=="manager":
                tasks.export_category_csv.delay(cid,user_id)
                return "Exported CSV send via email!"
            else:
                return "User operation not allowed"
        else:
            return "User not authorized"
    else:
        return "Invalid HTTP Request"