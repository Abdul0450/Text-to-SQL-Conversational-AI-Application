from dotenv import load_dotenv
load_dotenv() ##
import streamlit as st
import sqlite3
import google.generativeai as genai
import os 

## configure api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load google gemini Model and provide query as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content([prompt,question])
    return response.text

## Funcion to retrieve querty from the sql database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

### Define Your Prompt
prompt="""
     You are an expert in converting English questions into SQL queries.
    The SQL database table name is BILLS and it has the following columns:
    BILL_ITEM_ID (INTEGER, PRIMARY KEY, AUTOINCREMENT),
    PRODUCT_NAME (TEXT),
    INVOICE_DATE (TEXT in 'YYYY-MM-DD' format),
    TOTAL_AMOUNT (REAL),
    PAYMENT_STATUS (TEXT, values such as 'Cash', 'UPI', 'Pending'),
    QUANTITY (TEXT).

    Your task: Convert any English question into an accurate SQL query.
    
    Important Rules:
    - Return only the SQL query. Do not add explanations or extra text.
    - If user asks “how many” → use SELECT COUNT(*)
    - If user asks for total money → use SUM(TOTAL_AMOUNT)
    - If user says pending/unpaid → PAYMENT_STATUS = 'Pending'
    - If latest/recent → ORDER BY INVOICE_DATE DESC LIMIT 1
    - Match column names exactly as given above.

    Example1:
    English: How many bills are present in the database?
    SQL: SELECT COUNT(*) FROM BILLS;

    Example2:
    Show all pending bills
    SELECT * FROM BILLS WHERE PAYMENT_STATUS = 'Pending';

    Exaple3:
    Total amount collected by UPI
    SELECT SUM(TOTAL_AMOUNT) FROM BILLS WHERE PAYMENT_STATUS = 'UPI';

    Now wait for the English input and generate the SQL query only.


"""


#Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrive SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the Question")

# Now if submitte is click 

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"store.db")
    st.subheader("The respose is:")
    for row in data:
        print(row)
        st.header(row)