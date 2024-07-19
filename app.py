import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import calendar
from mysql.connector import Error
from data_processor import append_to_database, get_all_data, get_merchant_transactions, process_excel

st.set_page_config(page_title='HDFC Bank Statement Analysis', page_icon=':moneybag:', layout="wide")

# Custom CSS (same as before)
st.markdown("""
<style>
    /* Your custom CSS here */
</style>
""", unsafe_allow_html=True)

st.title('💼 HDFC Bank Statement Analyzer')
st.markdown("Visualize and analyze your HDFC Bank statement with ease.")

uploaded_file = st.sidebar.file_uploader("Choose an XLS format file of HDFC Bank Statement", type="xls")

if uploaded_file is not None:
    df = process_excel(uploaded_file)
    st.sidebar.success("File processed successfully!")
    
    if st.sidebar.button("Add to Database"):
        try:
            append_to_database(df)
            st.sidebar.success("Data added to database successfully!")
        except Error as e:
            st.sidebar.error(f"Error adding data to database: {e}")

# Get all data from the database
df = get_all_data()

if not df.empty:
    # Add month-year column for filtering
    df['MonthYear'] = pd.to_datetime(df['Date']).dt.to_period('M')
    
    # Month filter
    months = df['MonthYear'].unique()
    selected_month = st.sidebar.selectbox('Select Month', months, index=len(months)-1)
    
    # Filter data based on selected month
    df_filtered = df[df['MonthYear'] == selected_month]

    # Summary Statistics
    st.header("📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", f"{len(df_filtered):,}")
    with col2:
        st.metric("Total Withdrawal", f"₹{df_filtered['Withdrawal'].sum():,.2f}")
    with col3:
        st.metric("Total Deposit", f"₹{df_filtered['Deposited'].sum():,.2f}")
    with col4:
        st.metric("Net Change", f"₹{df_filtered['Deposited'].sum() - df_filtered['Withdrawal'].sum():,.2f}")

    # Withdrawals and Deposits
    st.header("💸 Withdrawals and Deposits")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_filtered['Date'], y=df_filtered['Withdrawal'], name='Withdrawals', marker_color='red'))
    fig.add_trace(go.Bar(x=df_filtered['Date'], y=df_filtered['Deposited'], name='Deposits', marker_color='green'))
    fig.update_layout(barmode='group', title='Withdrawals and Deposits Over Time')
    st.plotly_chart(fig, use_container_width=True)

    # Daily Spending Heatmap
    st.header("🗓️ Daily Spending Heatmap")
    df_filtered['DayOfWeek'] = pd.to_datetime(df_filtered['Date']).dt.dayofweek
    df_filtered['WeekOfMonth'] = pd.to_datetime(df_filtered['Date']).dt.day.apply(lambda x: (x-1)//7 + 1)
    daily_spending = df_filtered.groupby(['WeekOfMonth', 'DayOfWeek'])['Withdrawal'].sum().unstack()

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=daily_spending.values,
        x=[calendar.day_abbr[i] for i in range(7)],
        y=daily_spending.index,
        colorscale='YlOrRd'))
    fig_heatmap.update_layout(title='Daily Spending Heatmap', xaxis_title='Day of Week', yaxis_title='Week of Month')
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Monthly Income vs Expenses
    st.header("💹 Monthly Income vs Expenses")
    monthly_summary = df.groupby('MonthYear').agg({
        'Withdrawal': 'sum',
        'Deposited': 'sum'
    }).reset_index()
    monthly_summary['MonthYear'] = monthly_summary['MonthYear'].astype(str)

    fig_monthly = go.Figure(data=[
        go.Bar(name='Income', x=monthly_summary['MonthYear'], y=monthly_summary['Deposited']),
        go.Bar(name='Expenses', x=monthly_summary['MonthYear'], y=monthly_summary['Withdrawal'])
    ])
    fig_monthly.update_layout(barmode='group', title='Monthly Income vs Expenses')
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Spending Frequency
    st.header("🔄 Spending Frequency")
    transaction_counts = df_filtered['UPIs'].value_counts().head(10)
    fig_frequency = px.bar(transaction_counts, x=transaction_counts.index, y=transaction_counts.values, 
                           title='Top 10 Most Frequent Transaction Categories')
    fig_frequency.update_layout(xaxis_title="Category", yaxis_title="Number of Transactions")
    st.plotly_chart(fig_frequency, use_container_width=True)

    # Day of Week Analysis
    st.header("📅 Day of Week Analysis")
    day_of_week_spending = df_filtered.groupby('DayOfWeek')['Withdrawal'].mean().reindex(range(7))
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    fig_dow = px.bar(x=day_names, y=day_of_week_spending.values, 
                     title='Average Spending by Day of Week')
    fig_dow.update_layout(xaxis_title="Day of Week", yaxis_title="Average Spending (₹)")
    st.plotly_chart(fig_dow, use_container_width=True)

    # Merchant Transactions
    st.header("🏪 Merchant Transactions")
    merchant_df = get_merchant_transactions()
    st.dataframe(merchant_df)

    # Download merchant transactions
    csv = merchant_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merchant_transactions.csv">Download Merchant Transactions</a>'
    st.markdown(href, unsafe_allow_html=True)

else:
    st.info("Please upload an HDFC Bank statement XLS file and add it to the database to begin analysis.")

# Footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'Created with ❤️ by Your Name'; 
        visibility: visible;
        display: block;
        position: relative;
        padding: 15px;
        top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)