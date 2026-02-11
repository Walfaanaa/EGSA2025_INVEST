import streamlit as st
import pandas as pd
import altair as alt

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(
    page_title="EGSA2025 Loan Investment Simulator",
    layout="wide"
)

# ==========================
# CUSTOM CSS (WELCOME + GLOW + STARS)
# ==========================
st.markdown("""
<style>

/* ================= WELCOME STAR ANIMATION ================= */

@keyframes twinkle {
    0% { opacity: 0.2; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
    100% { opacity: 0.2; transform: scale(0.8); }
}

.welcome-container {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 20px;
}

.welcome-star {
    color: gold;
    animation: twinkle 2s infinite;
    display: inline-block;
    margin: 0 8px;
}

/* ================= Glow Switching ================= */

@keyframes glowSwitch {
    0% {
        background: radial-gradient(circle at left, rgba(255,0,0,0.35), transparent 60%),
                    radial-gradient(circle at right, rgba(0,255,0,0.35), transparent 60%);
    }
    50% {
        background: radial-gradient(circle at right, rgba(255,0,0,0.35), transparent 60%),
                    radial-gradient(circle at left, rgba(0,255,0,0.35), transparent 60%);
    }
    100% {
        background: radial-gradient(circle at left, rgba(255,0,0,0.35), transparent 60%),
                    radial-gradient(circle at right, rgba(0,255,0,0.35), transparent 60%);
    }
}

.logo-container {
    position: relative;
    display: flex;
    justify-content: center;
    padding: 60px;
    border-radius: 30px;
    animation: glowSwitch 10s infinite;
    overflow: hidden;
}

/* ================= Moving Stars Around Logo ================= */

@keyframes moveLeft {
    0%   { transform: translate(-180px, -40px); }
    50%  { transform: translate(-100px, 50px); }
    100% { transform: translate(-180px, -40px); }
}

@keyframes moveRight {
    0%   { transform: translate(180px, 40px); }
    50%  { transform: translate(100px, -50px); }
    100% { transform: translate(180px, 40px); }
}

.star {
    position: absolute;
    font-size: 22px;
    color: gold;
}

.star-left  { animation: moveLeft 6s ease-in-out infinite; }
.star-right { animation: moveRight 6s ease-in-out infinite; }

</style>
""", unsafe_allow_html=True)

# ==========================
# WELCOME HEADER
# ==========================
st.markdown("""
<div class="welcome-container">
    <span class="welcome-star">★</span>
    Welcome to EGSA2025 Investment Project
    <span class="welcome-star" style="animation-delay:1s;">★</span>
    <span class="welcome-star" style="animation-delay:2s;">★</span>
</div>
""", unsafe_allow_html=True)

# ==========================
# LOGO WITH EFFECTS
# ==========================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="star star-left">★</div>', unsafe_allow_html=True)
    st.markdown('<div class="star star-right">★</div>', unsafe_allow_html=True)

    st.image(
        "https://raw.githubusercontent.com/Walfaanaa/EGSA2025_INVEST/main/EGSA.png",
        use_column_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# DESCRIPTION
# ==========================
st.markdown(
    "<p style='text-align: center;'>Simulate investing a total amount across different loan types for a given duration (in months).</p>",
    unsafe_allow_html=True
)

st.divider()

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

    num_loans = capital // loan["Amount"]
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
st.dataframe(df, use_container_width=True)

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

