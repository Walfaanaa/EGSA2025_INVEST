import streamlit as st
import pandas as pd
import altair as alt

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="EGSA2025 Loan Investment Simulator", layout="wide")

# ==========================
# DISPLAY IMAGE AT TOP AND CENTER
# ==========================
# Create 3 columns, display image in the middle column
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://github.com/Walfaanaa/EGSA2025_INVEST/EGSA.png", use_column_width=True)

# ==========================
# TITLE & DESCRIPTION
# ==========================
st.title("💰 EGSA2025 Investment Strategy Simulator")
st.write("Simulate investing a total amount across different loan types for a given duration (in months).")

# ==========================
# USER INPUT
# ==========================
total_investment = st.number_input("Total Investment (birr):", value=150000, step=1000)
months = st.number_input("Investment Duration (months):", value=2, step=1)

# ==========================
# LOAN RULES
# ==========================
loans = [
    {"Loan Type": "Level_1", "Amount": 2000, "Interest": 0.05, "Duration_days": 7},
    {"Loan Type": "Level_2", "Amount": 5000, "Interest": 0.05, "Duration_days": 15},
    {"Loan Type": "Level_3", "Amount": 10000, "Interest": 0.10, "Duration_days": 30},
    {"Loan Type": "Level_4", "Amount": 15000, "Interest": 0.15, "Duration_days": 60},
]

# ==========================
# ALLOCATION STRATEGY
# ==========================
allocation = {
    "Level_1": 30000,
    "Level_2": 40000,
    "Level_3": 40000,
    "Level_4": 40000
}

# Adjust allocation proportionally if total != total_investment
total_alloc = sum(allocation.values())
if total_alloc != total_investment:
    scale = total_investment / total_alloc
    for k in allocation:
        allocation[k] = round(allocation[k] * scale)

# ==========================
# CALCULATE PROFIT
# ==========================
results = []

for loan in loans:
    loan_type = loan["Loan Type"]
    capital = allocation.get(loan_type, 0)
    num_loans = capital // loan["Amount"]  # integer number of loans that can be funded
    
    # total cycles over the investment period (fractional cycles allowed)
    cycles_total = (months * 30) / loan["Duration_days"]
    
    profit_per_loan = loan["Amount"] * loan["Interest"]
    total_profit = num_loans * profit_per_loan * cycles_total
    
    results.append({
        "Loan Type": loan_type,
        "Capital Allocated": capital,
        "# Loans": num_loans,
        "Profit per Loan per Cycle": profit_per_loan,
        "Cycles Total": round(cycles_total, 2),
        "Total Profit": round(total_profit, 2)
    })

df = pd.DataFrame(results)

# ==========================
# DISPLAY RESULTS
# ==========================
st.subheader("📊 Profit Simulation Table")
st.dataframe(df)

total_profit_all = df["Total Profit"].sum()
st.success(f"💵 Total Expected Profit for {months} month(s): {round(total_profit_all, 2)} birr")

# ==========================
# PROFIT CHART
# ==========================
chart = alt.Chart(df).mark_bar().encode(
    x='Loan Type',
    y='Total Profit',
    color='Loan Type',
    tooltip=['Loan Type', 'Capital Allocated', 'Total Profit']
).properties(
    title='Total Profit per Loan Type'
)

st.altair_chart(chart, use_container_width=True)
