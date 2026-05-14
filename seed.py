from app import create_app
from app.extensions import db
from app.models import User, Category, MonthlyTransaction, Transaction
from datetime import datetime

# Initialize the Flask application
app = create_app()

# Run database operations within the app context
with app.app_context():
    print("Clearing old data...")
    db.drop_all()   
    db.create_all() 

    print("Adding complete dummy data from Project 3...")

    # --- 1. Create Users ---
    users = [
        User(u_id='U001', first_name='Justin', last_name='Carlson', email='justin.carlson@example.com', creation_date=datetime(2026, 5, 7, 8, 0, 0)),
        User(u_id='U002', first_name='Andrew', last_name='Lathem', email='andrew.lathem@example.com', creation_date=datetime(2026, 5, 7, 9, 0, 0)),
        User(u_id='U003', first_name='Nate', last_name='Ankenbaur', email='nate.ankenbaur@example.com', creation_date=datetime(2026, 5, 7, 10, 0, 0)),
        User(u_id='U004', first_name='Viet', last_name='Nguyen', email='viet.nguyen@example.com', creation_date=datetime(2026, 5, 7, 11, 0, 0)),
        User(u_id='U005', first_name='Cole', last_name='Albert', email='cole.albert@example.com', creation_date=datetime(2026, 5, 7, 12, 0, 0))
    ]

    # --- 2. Create Categories ---
    categories = [
        Category(c_id='C01', c_name='Dining', c_desc='Dining out', c_goal=150.00, is_custom=False),
        Category(c_id='C02', c_name='Rent', c_desc='Monthly housing payment', c_goal=750.00, is_custom=False),
        Category(c_id='C03', c_name='Groceries', c_desc='House and food upkeep', c_goal=200.00, is_custom=False),
        Category(c_id='C04', c_name='Hobbies', c_desc='Gaming and sports', c_goal=100.00, is_custom=True),
        Category(c_id='C05', c_name='Travel', c_desc='Gas and tolls', c_goal=200.00, is_custom=False)
    ]

    # --- 3. Create Monthly Transactions ---
    monthly_transactions = [
        MonthlyTransaction(month=12, year=2025, month_goal=3000.00, last_updated=datetime(2025, 12, 31).date()),
        MonthlyTransaction(month=1, year=2026, month_goal=3000.00, last_updated=datetime(2026, 1, 31).date()),
        MonthlyTransaction(month=2, year=2026, month_goal=3500.00, last_updated=datetime(2025, 2, 28).date()),
        MonthlyTransaction(month=3, year=2026, month_goal=2700.00, last_updated=datetime(2025, 3, 31).date()),
        MonthlyTransaction(month=4, year=2026, month_goal=2800.00, last_updated=datetime(2025, 4, 30).date())
    ]

    # --- 4. Create Transactions ---
    transactions = [
        Transaction(
            t_id='T01', u_id='U001', c_id='C01', item_name='Dinner', 
            vendor_name="Freddy's", purchase_date=datetime(2025, 12, 20, 12, 30, 0), 
            t_amount=15.50, payment_method='Credit'
        ),
        Transaction(
            t_id='T02', u_id='U002', c_id='C02', item_name='Rent Payment', 
            vendor_name="Stoney Pointe", purchase_date=datetime(2025, 12, 31, 9, 0, 0), 
            t_amount=750.00, payment_method='Credit'
        ),
        Transaction(
            t_id='T03', u_id='U001', c_id='C04', item_name='Tomadachi Life: Living the Dream', 
            vendor_name="GameStop", purchase_date=datetime(2025, 12, 18, 2, 30, 0), 
            t_amount=60.00, payment_method='Cash'
        ),
        Transaction(
            t_id='T04', u_id='U003', c_id='C05', item_name='Gas', 
            vendor_name="Love's Travel Stop", purchase_date=datetime(2026, 1, 5, 4, 30, 0), 
            t_amount=41.00, payment_method='Tap2Pay'
        ),
        Transaction(
            t_id='T05', u_id='U004', c_id='C03', item_name='Chicken Parm ingredients', 
            vendor_name="Dillon's", purchase_date=datetime(2026, 1, 20, 6, 0, 0), 
            t_amount=30.00, payment_method='Debit'
        )
    ]

    # Stage all lists to be saved
    db.session.add_all(users)
    db.session.add_all(categories)
    db.session.add_all(monthly_transactions)
    db.session.add_all(transactions)

    # Commit the transaction to save them to the database
    db.session.commit()

    print("All tables successfully seeded!")