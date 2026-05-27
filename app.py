import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="Expense Analytics", page_icon="💸", layout="wide")
st.title("Expense Analytics Dashboard")
st.markdown("Automated expense analysis for personal finance tracking.")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])

if uploaded_file is not None:
    # 3. Load Data
    df = pd.read_csv(uploaded_file)
    
    # Merge Date and Time for chronological sorting
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
    # Split Income and Expenses
    expenses = df[df['Amount'] < 0].copy()
    expenses['Amount'] = expenses['Amount'].abs() 
    income = df[df['Amount'] > 0]

    # 4. KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Income", value=f"{income['Amount'].sum():,.0f} CZK")
    col2.metric(label="Total Expenses", value=f"{expenses['Amount'].sum():,.0f} CZK")
    col3.metric(label="Net Balance", value=f"{df['Amount'].sum():,.0f} CZK")

    st.divider()

    # 5. Dashboard Layout
    left_column, right_column = st.columns([2, 1])

    with left_column:
        st.subheader("📊 Spending by Category")
        category_spending = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(category_spending.index, category_spending.values, color='#4CAF50')
        ax.set_ylabel('Amount (CZK)')
        ax.set_title('Total Expenses per Category')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with right_column:
        st.subheader("📑 Filtered Transactions")
        selected_category = st.selectbox("Filter by Category", ["All"] + list(expenses['Category'].unique()))
        
        if selected_category == "All":
            filtered_df = expenses.copy()
        else:
            filtered_df = expenses[expenses['Category'] == selected_category].copy()
        
        # Formatting Date for display + Time
        filtered_df['Date'] = filtered_df['DateTime'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Display Table
        st.dataframe(filtered_df[['Date', 'Description', 'Amount']], hide_index=True)

else:
    st.info("Please upload your CSV file to begin the analysis.")