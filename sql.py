import sqlite3

## Connect to sqlite database
connection = sqlite3.connect("store.db")

## Craete a cursor  object  to insert records, create tables, relrieve 
coursor=connection.cursor()

##create a table
table_info="""
CREATE TABLE IF NOT EXISTS BILLS(
    BILL_ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PRODUCT_NAME TEXT NOT NULL,
    INVOICE_DATE TEXT NOT NULL,
    TOTAL_AMOUNT REAL,
    PAYMENT_STATUS TEXT NOT NULL DEFAULT 'Pending',
    QUANTITY TEXT NOT NULL
)
"""

coursor.execute(table_info)

## Insert some records 


coursor.execute("""
INSERT INTO BILLS (PRODUCT_NAME, INVOICE_DATE, TOTAL_AMOUNT, PAYMENT_STATUS, QUANTITY) VALUES
('Chana Dal', '2025-10-28', 180, 'Cash', '2kg'),
('Fortune Oil', '2025-10-27', 160, 'UPI', '1L'),
('Aashirvaad Atta', '2025-10-25', 320, 'Pending', '5kg'),
('Parle G Biscuit', '2025-10-22', 50, 'Cash', '5 Pack'),
('Tata Salt', '2025-10-20', 25, 'UPI', '1kg')
""")

## Dispaly all records 
print("This inserted records are:")

data= coursor.execute('''select * from BILLS''')

for row in data:
    print(row)

## Close the connection 

connection.commit()
connection.close()