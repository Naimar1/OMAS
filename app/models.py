from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    bought_id = db.Column(db.Integer,db.ForeignKey("boughts.id"))
    produts = db.relationship('Product',backref = 'user',lazy = "dynamic")
    boughts = db.relationship('Bought',backref = 'user',lazy = "dynamic")
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Bought(db.Model):
    __tablename__ = 'boughts'

    id = db.Column(db.Integer,primary_key = True)
    date_bought = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer,db.ForeignKey("products.id"))
    def save_bought(self):
        db.session.add(self)
        db.session.commit()

    def get_bought(id):
       bought = Bought.query.filter_by(id=id).first()
        return Bought

    
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key = True)
    product = db.Column(db.String(255))
    price= db.Column(db.Integer)
    description= db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    bought_id = db.Column(db.Integer,db.ForeignKey("boughts.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_products(cls,bought):
        products = Product.query.filter_by(bought=bought.id).all()
        return products

class Subscription(UserMixin, db.Model):
    __tablename__ = 'subs'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

def __repr__(self):
        return f'{self.email}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'
        


    