from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from .models import User, Category, Transaction, MonthlyTransaction
from .extensions import db
import uuid

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

# --- VIEW ALL TRANSACTIONS ---
@main.route('/transactions')
def transactions():
    all_transactions = Transaction.query.order_by(Transaction.purchase_date.asc()).all()
    return render_template('transactions.html', transactions=all_transactions)

# --- ADD TRANSACTION ---
@main.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date_str = request.form.get('purchase_date')
        parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        # --- NEW PURCHASER LOGIC ---
        selected_u_id = request.form.get('u_id')
        
        if selected_u_id == 'new':
            new_u_id = f"U_{uuid.uuid4().hex[:5].upper()}"
            new_user = User(
                u_id=new_u_id,
                first_name=request.form.get('new_first_name'),
                last_name=request.form.get('new_last_name'),
                email=request.form.get('new_email')
            )
            db.session.add(new_user)
            db.session.flush() # Save temporarily to get the ID
            selected_u_id = new_u_id

        # --- NEW CATEGORY LOGIC ---
        selected_c_id = request.form.get('c_id')
        
        if selected_c_id == 'new':
            new_c_id = f"C_{uuid.uuid4().hex[:5].upper()}"
            new_cat = Category(
                c_id=new_c_id,
                c_name=request.form.get('new_category_name'),
                c_desc='User created category',
                c_goal=0.0,
                is_custom=True
            )
            db.session.add(new_cat)
            db.session.flush() # Save temporarily to get the ID
            selected_c_id = new_c_id

        # --- CREATE TRANSACTION ---
        new_tx = Transaction(
            t_id=f"T_{uuid.uuid4().hex[:8].upper()}",
            u_id=selected_u_id, # Uses either the existing ID or the newly generated one
            c_id=selected_c_id, # Uses either the existing ID or the newly generated one
            item_name=request.form.get('item_name'),
            vendor_name=request.form.get('vendor_name'),
            purchase_date=parsed_date,
            t_amount=float(request.form.get('t_amount')),
            payment_method=request.form.get('payment_method')
        )
        db.session.add(new_tx)
        
        # Commit EVERYTHING (User, Category, Transaction) to the database
        db.session.commit() 
        
        flash("Transaction added successfully!", "success")
        return redirect(url_for('main.transactions'))
    
    categories = Category.query.all()
    users = User.query.all()
    return render_template('add_transaction.html', categories=categories, users=users)

# --- EDIT TRANSACTION ---
@main.route('/transactions/edit/<string:t_id>', methods=['GET', 'POST'])
def edit_transaction(t_id):
    transaction = Transaction.query.get_or_404(t_id)
    
    if request.method == 'POST':
        date_str = request.form.get('purchase_date')
        transaction.purchase_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        transaction.u_id = request.form.get('u_id')
        transaction.c_id = request.form.get('c_id')
        transaction.item_name = request.form.get('item_name')
        transaction.vendor_name = request.form.get('vendor_name')
        transaction.t_amount = float(request.form.get('t_amount'))
        transaction.payment_method = request.form.get('payment_method')
        
        db.session.commit()
        flash("Transaction updated successfully!", "success")
        return redirect(url_for('main.transactions'))

    categories = Category.query.all()
    users = User.query.all()
    return render_template('edit_transaction.html', transaction=transaction, categories=categories, users=users)

# --- DELETE TRANSACTION ---
@main.route('/transactions/delete/<string:t_id>', methods=['POST'])
def delete_transaction(t_id):
    tx = Transaction.query.get_or_404(t_id)
    db.session.delete(tx)
    db.session.commit()
    flash("Transaction deleted.", "danger")
    return redirect(url_for('main.transactions'))

# --- STATS PAGE ---
@main.route('/stats')
def stats():
    # SQLAlchemy grouping and sum logic goes here for budget calculations
    return render_template('stats.html')