from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Establish relationship to transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.String(50), primary_key=True)
    c_name = db.Column(db.String(50), nullable=False)
    c_desc = db.Column(db.String(200))
    c_goal = db.Column(db.Float)
    is_custom = db.Column(db.Boolean, default=False)

    transactions = db.relationship('Transaction', backref='category', lazy=True)

class MonthlyTransaction(db.Model):
    __tablename__ = 'monthly_transaction'
    month = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    month_goal = db.Column(db.Float)
    last_updated = db.Column(db.Date)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.String(50), primary_key=True)
    u_id = db.Column(db.String(50), db.ForeignKey('user.u_id'), nullable=False)
    c_id = db.Column(db.String(50), db.ForeignKey('category.c_id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    vendor_name = db.Column(db.String(100))
    purchase_date = db.Column(db.DateTime, nullable=False)
    t_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))

#class ExampleRecord(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(120), nullable=False)
#
#    def __repr__(self):
#        return f"<ExampleRecord {self.title}>"


