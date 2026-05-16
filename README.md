# Group Finance App

This project is aimed towards groups of people or friends that need to do monthly budgets together! Keep track of who is spending money on what and stay within a set limit for the month! (App is very well in its preliminary stages)

## Installation Setup
1. Create and activate a virtual environment.
   ```
   python -m venv .venv   
   .venv\Scripts\activate 
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start up the database before starting the app:
   ```bash
   python seed.py
   ```
4. Start the application:
   ```bash
   python run.py
   ```
5. Open http://127.0.0.1:5000

## Database Setup
The database should already be set up as you run the seed.py file. SQLAlchemy will build the database schema that is located in the models.py file. A .sql is also provided to show the SQL schema.

## How To Use The App
Once you start the app you will begin on the  **DEV PAGE**. This page will show you all the dummy data that was generated and pushed to the database. Here are the rest of the tabs and what they do:
* Transactions
   * This page will list all the transactions and let you edit and delete any transactions.
   * While editing, you may also add in any new users and/or categories for the transactions. The newly added users and categories will be present when adding in future transactions.
   * To EDIT -> click on EDIT button and fill out the fields and and click on SAVE CHANGES or CANCEL.
   * To DELETE -> click on DELETE and it will show a prompt to confirm deletion.
* Add New
   * This page just allows you to add new transactions and follows the same structure as the edit page.
* Stats
   * This page shows monthly stats such as how much for the month has been spent, how close total spent is to the goal, and which categories are the highest spent.
   * The page allows a user to go through different months as well.


## Notes

- This app is limited on features. Please keep this in mind when using.
- SQLite is used out of the box via `DATABASE_URL=sqlite:///app.db`.
- To switch databases, set `DATABASE_URL` (for example, PostgreSQL/MySQL URI) and install the corresponding driver.
- Tables are auto-created at startup for this minimal starter (`db.create_all()`).
