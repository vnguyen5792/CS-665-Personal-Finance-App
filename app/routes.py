from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import extract, func
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
    return render_template("index.html", users=users, categories=categories, transactions=transactions, monthly_transaction=monthly_transactions)

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
    tx = Transaction.query.get_or_404(t_id)
    
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
            db.session.flush() 
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
            db.session.flush() 
            selected_c_id = new_c_id

        # --- UPDATE EXISTING TRANSACTION ---
        tx.u_id = selected_u_id
        tx.c_id = selected_c_id
        tx.item_name = request.form.get('item_name')
        tx.vendor_name = request.form.get('vendor_name')
        tx.purchase_date = parsed_date
        tx.t_amount = float(request.form.get('t_amount'))
        tx.payment_method = request.form.get('payment_method')
        
        db.session.commit()
        
        flash("Transaction updated successfully!", "success")
        return redirect(url_for('main.transactions'))

    categories = Category.query.all()
    users = User.query.all()
    return render_template('edit_transaction.html', transaction=tx, categories=categories, users=users)

# --- DELETE TRANSACTION ---
@main.route('/transactions/delete/<string:t_id>', methods=['POST'])
def delete_transaction(t_id):
    tx = Transaction.query.get_or_404(t_id)
    db.session.delete(tx)
    db.session.commit()
    flash("Transaction deleted.", "danger")
    return redirect(url_for('main.transactions'))

# --- CREATE MONTHLY BUDGET ---
@main.route('/monthly/add', methods=['GET', 'POST'])
def add_monthly():
    if request.method == 'POST':
        m = int(request.form.get('month'))
        y = int(request.form.get('year'))
        
        # Prevent database crashes by checking if this month/year combo already exists!
        existing = MonthlyTransaction.query.filter_by(month=m, year=y).first()
        if existing:
            flash(f"A budget for {m}/{y} already exists! Please edit it instead.", "danger")
            return redirect(url_for('main.add_monthly'))

        new_mt = MonthlyTransaction(
            month=m,
            year=y,
            month_goal=float(request.form.get('month_goal')),
            last_updated=datetime.utcnow().date()
        )
        db.session.add(new_mt)
        db.session.commit()
        
        flash(f"Monthly budget for {m}/{y} created successfully!", "success")
        return redirect(url_for('main.index'))
    
    return render_template('add_monthly.html')

# --- EDIT MONTHLY BUDGET ---
@main.route('/monthly/edit/<int:year>/<int:month>', methods=['GET', 'POST'])
def edit_monthly(year, month):
    # Query using the composite key
    mt = MonthlyTransaction.query.filter_by(year=year, month=month).first_or_404()
    
    if request.method == 'POST':
        # We don't let them change the month/year here, only the goal amount
        mt.month_goal = float(request.form.get('month_goal'))
        mt.last_updated = datetime.utcnow().date()
        
        db.session.commit()
        flash(f"Budget goal for {month}/{year} updated!", "success")
        return redirect(url_for('main.index'))
        
    return render_template('edit_monthly.html', mt=mt)

# --- DELETE MONTHLY BUDGET ---
@main.route('/monthly/delete/<int:year>/<int:month>', methods=['POST'])
def delete_monthly(year, month):
    mt = MonthlyTransaction.query.filter_by(year=year, month=month).first_or_404()
    
    db.session.delete(mt)
    db.session.commit()
    
    flash(f"Budget for {month}/{year} deleted.", "success")
    return redirect(url_for('main.index'))

@main.route('/stats')
def stats():
    # 1. Grab EVERY month to populate the dropdown menu
    all_months = MonthlyTransaction.query.order_by(
        MonthlyTransaction.year.desc(), 
        MonthlyTransaction.month.desc()
    ).all()

    if not all_months:
        flash("No monthly budgets found. Please add one first.", "info")
        return redirect(url_for('main.index'))

    # 2. Check if the user selected a specific period from the dropdown
    requested_period = request.args.get('period')
    
    if requested_period:
        # Split "4-2026" into month=4, year=2026
        req_month, req_year = map(int, requested_period.split('-'))
        target_mt = MonthlyTransaction.query.filter_by(month=req_month, year=req_year).first()
        
        # Fallback just in case they mess with the URL manually
        if not target_mt:
            target_mt = all_months[0]
    else:
        # Default to the most recent month
        target_mt = all_months[0]

    # 3. Calculate Total Spent for the TARGET month
    current_txs = Transaction.query.filter(
        extract('year', Transaction.purchase_date) == target_mt.year,
        extract('month', Transaction.purchase_date) == target_mt.month
    ).all()
    
    total_spent = sum(t.t_amount for t in current_txs)
    
    # 4. Budget Math
    budget = target_mt.month_goal
    remaining = budget - total_spent
    percent_used = (total_spent / budget) * 100 if budget > 0 else 0 

    # 5. Group by Category for the TARGET month
    category_stats = db.session.query(
        Category.c_name,
        func.sum(Transaction.t_amount).label('total_amount')
    ).join(Transaction, Category.c_id == Transaction.c_id)\
     .filter(
        extract('year', Transaction.purchase_date) == target_mt.year,
        extract('month', Transaction.purchase_date) == target_mt.month
     )\
     .group_by(Category.c_name)\
     .order_by(func.sum(Transaction.t_amount).desc())\
     .all()

    return render_template(
        'stats.html', 
        target_mt=target_mt, 
        all_months=all_months, # We pass this to build the dropdown menu!
        total_spent=total_spent, 
        remaining=remaining, 
        percent_used=percent_used,
        category_stats=category_stats
    )