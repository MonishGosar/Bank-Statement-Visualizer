import pandas as pd
from database import create_connection
from mysql.connector import Error
from datetime import datetime

def process_excel(file):
    df = pd.read_excel(file, sheet_name=0, engine='xlrd')
    df = df.iloc[21:-18]
    df = df.drop(df.columns[[0, 2]], axis=1)
    df = df.drop(df.index[1])
    df = df.fillna(0)
    df.rename(
        columns={'Unnamed: 1': 'UPIs', 'Unnamed: 3': 'Date', 'Unnamed: 4': 'Withdrawal', 'Unnamed: 5': 'Deposited',
                 'Unnamed: 6': 'Balance'},
        inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.date
    df['Withdrawal'] = pd.to_numeric(df['Withdrawal'], errors='coerce')
    df['Deposited'] = pd.to_numeric(df['Deposited'], errors='coerce')
    df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
    df['UPIs'] = df['UPIs'].astype(str)
    df['UPIs'] = df['UPIs'].str.split('@', expand=True)[0]
    df['UPIs'] = df['UPIs'].str.split('-', expand=True)[1]
    
    return df

def append_to_database(df):
    conn = create_connection()
    cursor = conn.cursor()

    # Get the last date in the database
    cursor.execute("SELECT MAX(date) FROM transactions")
    last_date = cursor.fetchone()[0]
    
    if last_date:
        df = df[df['Date'] > last_date]

    if not df.empty:
        for _, row in df.iterrows():
            query = """INSERT INTO transactions (date, upi, withdrawal, deposited, balance) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (row['Date'], row['UPIs'], row['Withdrawal'], row['Deposited'], row['Balance'])
            cursor.execute(query, values)
        
        conn.commit()
        print(f"Appended {len(df)} new transactions.")
    else:
        print("No new transactions to append.")

    conn.close()

def get_all_data():
    conn = create_connection()
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_merchant_transactions():
    conn = create_connection()
    query = """
        SELECT UPIs as Merchant, SUM(Withdrawal) as TotalAmount, 
               GROUP_CONCAT(Date ORDER BY Date) as TransactionDates
        FROM transactions
        WHERE Withdrawal > 0
        GROUP BY UPIs
        ORDER BY TotalAmount DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df