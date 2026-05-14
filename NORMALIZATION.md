# Project 3 Normalization Work
*NOTE: The Zybook submission of Project 2 differs from the blackboard submission due to the acknowledgement of the constraints listed in Zybook. For the purpose of Project 3, I will be using the Zybook submited database*

Below are the tables from Project 2:

### User

| u_id | first_name | last_name | email | creation_date |
| :--- | :--- | :--- | :--- | :--- |
| U001 | Justin | Carlson | justin.carlson@example.com | 2026-05-07 08:00:00 |
| U002 | Andrew | Lathem | andrew.lathem@example.com | 2026-05-07 09:00:00 |
| U003 | Nate | Ankenbaur | nate.ankenbaur@example.com | 2026-05-07 10:00:00 |
| U004 | Viet | Nguyen | viet.nguyen@example.com | 2026-05-07 11:00:00 |
| U005 | Cole | Albert | cole.albert@example.com | 2026-05-07 12:00:00 |


### Category

| c_id | c_name | c_desc | c_goal | is_custom |
| :--- | :--- | :--- | :--- | :--- |
| C01 | Dining | Dining out | 150.00 | 0 |
| C02 | Rent | Monthly housing payment | 750.00 | 0 |
| C03 | Groceries | House and food upkeep | 200.00 | 0 |
| C04 | Hobbies | Gaming and sports | 100.00 | 1 |
| C05 | Travel | Gas and tolls | 200.00 | 0 |


### Monthly Transaction

| mt_id | month | year | month_goal | last_updated |
| :--- | :--- | :--- | :--- | :--- |
| MT01 | 12 | 2025 | 3000.00 | 2025-12-31 |
| MT02 | 1 | 2026 | 3000.00 | 2026-01-31 |
| MT03 | 2 | 2026 | 3500.00 | 2025-02-28 |
| MT04 | 3 | 2026 | 2700.00 | 2025-03-31 |
| MT05 | 4 | 2026 | 2800.00 | 2025-04-30 |


### Transaction

| t_id | u_id | c_id | mt_id | item_name | vendor_name | purchase_date | t_amount | payment_method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T01 | U001 | C01 | MT01 | Dinner | Freddy's | 2025-12-20 12:30:00 | 15.50 | Credit |
| T02 | U002 | C02 | MT01 | Rent Payment | Stoney Pointe | 2025-12-31 09:00:00 | 750.00 | Credit |
| T03 | U001 | C04 | MT01 | Tomadachi Life: Living the Dream | GameStop | 2025-12-18 02:30:00 | 60.00 | Cash |
| T04 | U003 | C05 | MT02 | Gas | Love's Travel Stop | 2026-01-05 04:30:00 | 41.00 | Tap2Pay |
| T05 | U004 | C03 | MT02 | Chicken Parm ingredients | Dillon's | 2026-01-20 06:00:00 | 30.00 | Debit |

## Functional Dependacies
* User Table: u_id --> first_name, last_name, email, creation_date
* Category Table: c_id --> c_name, c_desc, c_goal, is_custom
* Monthly Transaction Table: mt_id --> month, year, month_goal, last_updated
* Transaction Table: t_id --> u_id, c_id, mt_id, item_name, vendor_name, purchase_date, t_amount, payment_method

## Anomolies
* UPDATE: updating purchase_date without updating mt_id creates a data mismatch
* INSERT, DELETE: there are no anomolies regarding insertion and deletion

## Solution
To solve the anomoly issue, the mt_id will be removed and the PK will consist of the month and year as a composite key. To join the monthly transaction table to transaction, the join will refer to the month and year of the purchase_date variable.

## New Schema
*NOTE: everything will remain the same except for the **Monthly Transaction** and **Transaction** table*

### MonthlyTransaction

| month | year | month_goal | last_updated |
| :--- | :--- | :--- | :--- |
| 12 | 2025 | 3000.00 | 2025-12-31 |
| 1 | 2026 | 3000.00 | 2026-01-31 |
| 2 | 2026 | 3500.00 | 2025-02-28 |
| 3 | 2026 | 2700.00 | 2025-03-31 |
| 4 | 2026 | 2800.00 | 2025-04-30 |

### Transaction

| t_id | u_id | c_id  | item_name | vendor_name | purchase_date | t_amount | payment_method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T01 | U001 | C01 | Dinner | Freddy's | 2025-12-20 12:30:00 | 15.50 | Credit |
| T02 | U002 | C02 | Rent Payment | Stoney Pointe | 2025-12-31 09:00:00 | 750.00 | Credit |
| T03 | U001 | C04 | Tomadachi Life: Living the Dream | GameStop | 2025-12-18 02:30:00 | 60.00 | Cash |
| T04 | U003 | C05 | Gas | Love's Travel Stop | 2026-01-05 04:30:00 | 41.00 | Tap2Pay |
| T05 | U004 | C03 | Chicken Parm ingredients | Dillon's | 2026-01-20 06:00:00 | 30.00 | Debit |