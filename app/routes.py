from flask import Blueprint, render_template

from .models import User, Category, Transaction, MonthlyTransaction
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    #records = ExampleRecord.query.order_by(ExampleRecord.id.desc()).all()
    #return render_template("index.html", records=records)
    users = User.query.order_by(User.u_id.asc()).all()
    categories = Category.query.order_by(Category.c_id.asc()).all()
    transactions = Transaction.query.order_by(Transaction.t_id.asc()).all()
    monthly_transactions = MonthlyTransaction.query.order_by(MonthlyTransaction.year.asc(), MonthlyTransaction.month.asc()).all()
    return render_template("index.html", users=users, categories=categories, transactions=transactions, monthly_transactions=monthly_transactions)