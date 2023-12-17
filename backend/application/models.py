from .database import *

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(10), nullable=False)
    items = db.relationship("Booking", backref = "user")
    approved=db.Column(db.Boolean, default=False)

    def to_dict(self):
        return{
            "id":self.id,
            "fname":self.fname,
            "lname":self.lname,
            "username":self.username,
        }



class ApproveCategory(db.Model):
    __tablename__ = "approvecategories"
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.cid", ondelete = "CASCADE"))
    cname = db.Column(db.String(150))
    updated_cname=db.Column(db.String(150))
    request_type=db.Column(db.String(150))
    manager_id=db.Column(db.String(150))

    def to_dict(self):
        return {
            "id":self.id,
            "category_id":self.category_id,
            "cname":self.cname,
            "updated_cname":self.updated_cname,
            "request_type":self.request_type,
            "manager_id":self.manager_id
        }
   
class Category(db.Model):
    __tablename__ = "categories"
    cid = db.Column(db.Integer, primary_key = True)
    cname = db.Column(db.String(150), unique=True)
    products = db.relationship("Product", backref = "category", cascade = "all, delete", passive_deletes = True)
    
    def to_dict(self):
        return {
            "cid":self.cid,
            "cname":self.cname,
            "products":[product.to_dict() for product in self.products]
        }
class Product(db.Model):
    __tablename__ = "products"
    pid = db.Column(db.Integer, primary_key = True)
    pname = db.Column(db.String(50), unique=True)
    manf_date = db.Column(db.Date)
    exp_date = db.Column(db.Date)
    unit = db.Column(db.String(10))
    rateperunit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.cid", ondelete = "CASCADE"))
    bookings = db.relationship("Booking", backref = "product", cascade = "all, delete", passive_deletes = True)

    def to_booking_dict(self):
        return {
            "pid":self.pid,
            "pname":self.pname,
            "manf_date":self.manf_date,
            "exp_date":self.exp_date,
            "unit":self.unit,
            "rateperunit":self.rateperunit,
            "quantity":self.quantity,
        }
    def to_dict(self):
        cname=Category.query.filter_by(cid=self.category_id).first().cname
        return {
            "pid":self.pid,
            "pname":self.pname,
            "manf_date":self.manf_date,
            "exp_date":self.exp_date,
            "unit":self.unit,
            "rateperunit":self.rateperunit,
            "quantity":self.quantity,
            "cname":cname,
            "bookings":[booking.to_dict() for booking in self.bookings]
        }

class Booking(db.Model):
    bookingid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.pid', ondelete = "CASCADE"))
    category_name = db.Column(db.String(50))
    quantity_of_item = db.Column(db.Integer)
    item_name = db.Column(db.String(50))

    def to_dict(self):
        product=Product.query.filter_by(pid=self.product_id).first()

        return {
            "bookingid":self.bookingid,
            "user_id":self.user_id,
            "product_id":self.product_id,
            "category_name":self.category_name,
            "quantity_of_item":self.quantity_of_item,
            "item_name":self.item_name,
            "product":product.to_booking_dict()
            

        }

class Order(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    productid = db.Column(db.Integer)
    totalprice = db.Column(db.Integer)
    quantity_of_product = db.Column(db.Integer)
    product_unit = db.Column(db.String(10))
    product_name = db.Column(db.String(50))

    def to_dict(self):
        return {
            "orderid":self.orderid,
            "userid":self.userid,
            "productid":self.productid,
            "totalprice":self.totalprice,
            "quantity_of_product":self.quantity_of_product,
            "product_unit":self.product_unit,
            "product_name":self.product_name
        }

class Token(db.Model):
    __tablename__ = "token"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)

class Visited(db.Model):
    user_id=db.Column(db.Integer, primary_key=True, nullable=False)
    status=db.Column(db.Boolean, nullable=False, default=False)