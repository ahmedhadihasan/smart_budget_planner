"""
Smart Budget Planner - Modern Web Application using Streamlit
A beautiful web-based interface for personal finance management with AI features
Run with: streamlit run budget_app_web.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import LabelEncoder

# Page configuration
st.set_page_config(
    page_title="Smart Budget Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling with Bzwen brand colors
st.markdown("""
<style>
    /* Main background with subtle gradient */
    .main {
        background: linear-gradient(135deg, #FFFEF5 0%, #FFFCF0 100%);
    }
    
    /* Modern sidebar with glass morphism effect */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFEF8 0%, #FFF9E6 50%, #FFECB3 100%);
        border-right: 1px solid rgba(255, 215, 6, 0.2);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: radial-gradient(circle at 50% 0%, rgba(255, 215, 6, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #000000;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }
    
    /* Metric cards */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(255, 215, 6, 0.2);
        border-left: 4px solid #FFD706;
    }
    
    .stMetric label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #000000;
    }
    
    /* Headers */
    h1 {
        color: #000000;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(255, 215, 6, 0.3);
    }
    
    h2, h3 {
        color: #000000;
        font-weight: 600;
    }
    
    /* All buttons with consistent styling */
    .stButton>button {
        background: linear-gradient(135deg, #FFD706 0%, #FFC107 100%);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(255, 215, 6, 0.3);
        width: 100%;
        min-height: 48px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%);
        box-shadow: 0 6px 12px rgba(255, 215, 6, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Ultra-modern sidebar navigation with pill design */
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
        display: flex;
        flex-direction: column;
        padding: 10px;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border: none;
        border-radius: 20px;
        padding: 18px 24px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 700;
        font-size: 17px;
        color: #000000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] .stRadio label::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: #FFD706;
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.9);
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 16px rgba(255, 215, 6, 0.25);
    }
    
    [data-testid="stSidebar"] .stRadio label:hover::before {
        transform: scaleY(1);
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #FFD706 0%, #FFC107 100%);
        box-shadow: 0 6px 20px rgba(255, 215, 6, 0.5), inset 0 1px 0 rgba(255,255,255,0.3);
        transform: translateX(12px) scale(1.05);
        font-weight: 800;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"]::before {
        width: 6px;
        background: #000000;
        transform: scaleY(1);
    }
    
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        display: none;
    }
    
    /* Add emoji spacing */
    [data-testid="stSidebar"] .stRadio label > div {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 215, 6, 0.1);
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        color: #000000;
        font-weight: 600;
        padding: 12px 24px;
        border: 2px solid #FFD706;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD706 0%, #FFC107 100%);
        color: #000000;
    }
    
    /* Info boxes with brand colors */
    .success-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 4px solid #4CAF50;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFECB3 100%);
        border-left: 4px solid #FFD706;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #FFD706 0%, #FFC107 100%);
        color: #000000;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(255, 215, 6, 0.3);
        border: none;
    }
    
    .info-box h3, .info-box h4 {
        color: #000000 !important;
        margin-top: 0;
    }
    
    .info-box strong {
        color: #000000;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea {
        border: 2px solid #FFD706;
        border-radius: 8px;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>div:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #FFC107;
        box-shadow: 0 0 0 2px rgba(255, 215, 6, 0.2);
    }
    
    /* Dataframe styling */
    .dataframe {
        border: 2px solid #FFD706 !important;
        border-radius: 10px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD706 0%, #FFC107 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Year', 'Month', 'Date', 'Category', 'Amount', 'Description'])
if 'salary' not in st.session_state:
    st.session_state.salary = 0
if 'budgets' not in st.session_state:
    st.session_state.budgets = {}
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'salary_history' not in st.session_state:
    st.session_state.salary_history = {}
if 'emergency_fund_target' not in st.session_state:
    st.session_state.emergency_fund_target = 300

# Constants
CATEGORIES = ['Food', 'Transportation', 'Entertainment', 'Shopping', 'Bills', 'Healthcare', 'Education', 'Other']
MONTH_NAMES = ['', 'January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Helper functions
def generate_salary_history(base_salary):
    """Generate 24-month salary history"""
    salary_history = {}
    for months_ago in range(23, -1, -1):
        date = datetime.now() - timedelta(days=months_ago * 30)
        year = date.year
        month = date.month
        
        years_back = (datetime.now().year - year) + (1 if datetime.now().month < 8 and month >= 8 else 0)
        hist_salary = base_salary / (1.15 ** years_back)
        
        month_key = f"{year}-{month:02d}"
        salary_history[month_key] = hist_salary
    
    return salary_history

def generate_sample_data():
    """Generate sample expenses for testing"""
    if st.session_state.salary == 0:
        st.error("Please set your salary first!")
        return
    
    expenses = []
    for months_ago in range(5, -1, -1):
        date = datetime.now() - timedelta(days=months_ago * 30)
        year = date.year
        month = date.month
        
        for _ in range(random.randint(30, 50)):
            category = random.choice(CATEGORIES)
            budget = st.session_state.budgets.get(category, 100)
            amount = round(random.uniform(budget * 0.05, budget * 0.3), 2)
            
            day = random.randint(1, 28)
            date_str = f"{year}-{month:02d}-{day:02d}"
            
            expenses.append({
                'Year': year,
                'Month': month,
                'Date': date_str,
                'Category': category,
                'Amount': amount,
                'Description': f"{category} expense"
            })
    
    new_df = pd.DataFrame(expenses)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_df], ignore_index=True)
    st.success(f"✓ Generated {len(expenses)} sample expenses for last 6 months!")

# Header with brand colors
st.markdown("""
<div style='background: linear-gradient(135deg, #FFD706 0%, #FFC107 100%); 
            padding: 35px; border-radius: 15px; margin-bottom: 30px;
            box-shadow: 0 6px 12px rgba(255, 215, 6, 0.4);'>
    <h1 style='color: #000000; margin: 0; font-size: 42px; font-weight: 800;'>💰 Smart Budget Planner</h1>
    <p style='color: #000000; font-size: 20px; margin: 10px 0 0 0; font-weight: 600;'>
        AI-Powered Personal Finance Manager
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation with improved styling
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigation menu with modern button-style radio buttons
    page = st.radio(
        "Select Page",
        [
            "📊 Dashboard",
            "⚙️ Setup",
            "💳 Expenses",
            "📈 Analysis",
            "🎯 Goals",
            "🤖 AI Insights"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    if st.session_state.salary > 0:
        st.metric("Monthly Salary", f"${st.session_state.salary:,.2f}")
    
    if not st.session_state.expenses.empty:
        total_expenses = st.session_state.expenses['Amount'].sum()
        st.metric("Total Expenses", f"${total_expenses:,.2f}")
        
        if st.session_state.salary > 0:
            # Calculate income from salary history or current salary
            total_income = 0
            if st.session_state.salary_history:
                total_income = sum(st.session_state.salary_history.values())
            else:
                months = len(st.session_state.expenses['Month'].unique())
                total_income = st.session_state.salary * months
            
            savings = max(0, total_income - total_expenses)  # Never negative
            st.metric("Total Savings", f"${savings:,.2f}")
    
    st.metric("Active Goals", len(st.session_state.goals))

# Main content based on selected page
if page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    if st.session_state.expenses.empty:
        st.info("👋 Welcome! Start by setting up your salary and adding expenses.")
    else:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_expenses = st.session_state.expenses['Amount'].sum()
        avg_expense = st.session_state.expenses['Amount'].mean()
        transaction_count = len(st.session_state.expenses)
        months_tracked = len(st.session_state.expenses['Month'].unique())
        
        with col1:
            st.metric("Total Spent", f"${total_expenses:,.2f}", 
                     f"{transaction_count} transactions")
        
        with col2:
            st.metric("Avg Transaction", f"${avg_expense:.2f}",
                     f"{months_tracked} months tracked")
        
        with col3:
            if st.session_state.salary > 0:
                # Calculate income based on salary history (realistic calculation)
                total_income = 0
                if st.session_state.salary_history:
                    # Use actual salary history
                    total_income = sum(st.session_state.salary_history.values())
                else:
                    # Fallback: assume current salary for tracked months
                    total_income = st.session_state.salary * months_tracked
                
                savings = max(0, total_income - total_expenses)  # Never show negative savings
                savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
                st.metric("Total Savings", f"${savings:,.2f}",
                         f"{savings_rate:.1f}% rate")
            else:
                st.metric("Total Savings", "$0", "Set salary first")
        
        with col4:
            st.metric("Active Goals", len(st.session_state.goals),
                     "financial targets")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Category Breakdown")
            category_totals = st.session_state.expenses.groupby('Category')['Amount'].sum()
            fig = px.pie(values=category_totals.values, names=category_totals.index,
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Spending Trend")
            monthly = st.session_state.expenses.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
            monthly['Period'] = monthly.apply(lambda x: f"{MONTH_NAMES[int(x['Month'])]} {int(x['Year'])}", axis=1)
            
            fig = px.line(monthly, x='Period', y='Amount', markers=True)
            fig.update_traces(line_color='#4CAF50', line_width=3, marker=dict(size=10))
            fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Setup":
    st.header("⚙️ Salary & Budget Setup")
    
    # Monthly Salary section (full width)
    st.subheader("💵 Monthly Salary")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        salary_input = st.number_input("Enter your monthly salary:", 
                                       min_value=0.0, value=float(st.session_state.salary),
                                       step=100.0, format="%.2f")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Set Salary", type="primary", use_container_width=True):
            st.session_state.salary = salary_input
            
            # Calculate budgets (80% of salary)
            total_budget = salary_input * 0.80
            percentages = {
                'Food': 0.30, 'Transportation': 0.15, 'Entertainment': 0.10,
                'Shopping': 0.10, 'Bills': 0.15, 'Healthcare': 0.05,
                'Education': 0.02, 'Other': 0.02
            }
            
            for category, pct in percentages.items():
                st.session_state.budgets[category] = total_budget * pct
            
            st.session_state.salary_history = generate_salary_history(salary_input)
            
            st.success(f"✓ Salary set to ${salary_input:,.2f}")
            st.success(f"✓ Budget: ${total_budget:,.2f} (80%)")
            st.success(f"✓ Planned savings: ${salary_input * 0.20:,.2f} (20%)")
            st.rerun()
    
    st.markdown("---")
    
    # Category Budgets section (full width)
    st.subheader("📊 Category Budgets")
    
    if st.session_state.budgets:
        budget_df = pd.DataFrame([
            {'Category': cat, 'Monthly Budget': f"${amount:.2f}", 
             'Percentage': f"{(amount/sum(st.session_state.budgets.values()))*100:.1f}%"}
            for cat, amount in st.session_state.budgets.items()
        ])
        
        st.dataframe(budget_df, use_container_width=True, hide_index=True)
        
        total = sum(st.session_state.budgets.values())
        savings = st.session_state.salary - total
        
        st.markdown(f"""
        <div class='info-box'>
            <strong>Budget Summary:</strong><br>
            Total Budget: ${total:,.2f} (80% of salary)<br>
            Planned Savings: ${savings:,.2f} (20% of salary)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Set your salary to auto-calculate category budgets")

elif page == "💳 Expenses":
    st.header("💳 Expense Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📁 Import CSV", "🎲 Generate Sample"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            expense_date = st.date_input("Date", datetime.now())
            expense_category = st.selectbox("Category", CATEGORIES)
            
        with col2:
            expense_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
            expense_desc = st.text_input("Description", f"{expense_category} expense")
        
        if st.button("Add Expense", type="primary"):
            if expense_amount > 0:
                new_expense = pd.DataFrame([{
                    'Year': expense_date.year,
                    'Month': expense_date.month,
                    'Date': expense_date.strftime("%Y-%m-%d"),
                    'Category': expense_category,
                    'Amount': expense_amount,
                    'Description': expense_desc
                }])
                
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], 
                                                      ignore_index=True)
                st.success(f"✓ Added ${expense_amount:.2f} to {expense_category}!")
                st.rerun()
            else:
                st.error("Please enter a valid amount!")
    
    with tab2:
        st.info("Import expenses from a CSV file (Date, Category, Amount, Description)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        with col2:
            replace_existing = st.checkbox("Replace existing data", value=False)
        
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                
                required_cols = ['Date', 'Category', 'Amount']
                if all(col in imported_df.columns for col in required_cols):
                    # Preview
                    st.write(f"**Preview:** {len(imported_df)} rows found")
                    st.dataframe(imported_df.head(10), use_container_width=True)
                    
                    if st.button("Import CSV", type="primary"):
                        valid_rows = []
                        
                        for _, row in imported_df.iterrows():
                            try:
                                date_obj = pd.to_datetime(row['Date'])
                                if row['Category'] in CATEGORIES and float(row['Amount']) > 0:
                                    valid_rows.append({
                                        'Year': date_obj.year,
                                        'Month': date_obj.month,
                                        'Date': str(row['Date']),
                                        'Category': row['Category'],
                                        'Amount': float(row['Amount']),
                                        'Description': str(row.get('Description', row['Category']))
                                    })
                            except:
                                continue
                        
                        if valid_rows:
                            new_df = pd.DataFrame(valid_rows)
                            
                            if replace_existing:
                                st.session_state.expenses = new_df
                                st.success(f"✓ Replaced with {len(valid_rows)} expenses!")
                            else:
                                st.session_state.expenses = pd.concat([st.session_state.expenses, new_df], 
                                                                      ignore_index=True)
                                # Remove duplicates based on Date, Category, Amount
                                st.session_state.expenses = st.session_state.expenses.drop_duplicates(
                                    subset=['Date', 'Category', 'Amount'], keep='first'
                                )
                                st.success(f"✓ Added {len(valid_rows)} new expenses (duplicates removed)!")
                            st.rerun()
                        else:
                            st.error("No valid expenses found in CSV!")
                else:
                    st.error(f"CSV must have columns: {', '.join(required_cols)}")
            
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
    
    with tab3:
        st.info("Generate realistic sample expenses for last 6 months")
        
        if st.button("Generate Sample Data", type="primary"):
            generate_sample_data()
            st.rerun()
    
    # Display expenses table
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📋 Recent Expenses")
    with col2:
        if not st.session_state.expenses.empty:
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.button("⚠️ Confirm Clear", type="secondary"):
                    st.session_state.expenses = pd.DataFrame(columns=['Year', 'Month', 'Date', 'Category', 'Amount', 'Description'])
                    st.success("✓ All expenses cleared!")
                    st.rerun()
    
    if not st.session_state.expenses.empty:
        # Show total count
        st.info(f"📊 Showing last 50 of **{len(st.session_state.expenses):,} total expenses**")
        
        display_df = st.session_state.expenses.tail(50).sort_values('Date', ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download button
        col1, col2 = st.columns(2)
        with col1:
            csv = st.session_state.expenses.to_csv(index=False)
            st.download_button(
                label="📥 Download All Expenses (CSV)",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        with col2:
            if st.button("🗑️ Delete All Expenses"):
                st.session_state.expenses = pd.DataFrame(columns=['Year', 'Month', 'Date', 'Category', 'Amount', 'Description'])
                st.success("✓ All expenses deleted!")
                st.rerun()
    else:
        st.info("No expenses yet. Add some to get started!")

elif page == "📈 Analysis":
    st.header("📈 Spending Analysis")
    
    if st.session_state.expenses.empty:
        st.warning("No expenses to analyze. Please add expenses first!")
    else:
        # Summary statistics
        total_spent = st.session_state.expenses['Amount'].sum()
        total_transactions = len(st.session_state.expenses)
        avg_transaction = st.session_state.expenses['Amount'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"${total_spent:,.2f}")
        col2.metric("Transactions", f"{total_transactions:,}")
        col3.metric("Avg Transaction", f"${avg_transaction:.2f}")
        
        st.markdown("---")
        
        # Category analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Category Breakdown")
            cat_totals = st.session_state.expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            
            fig = go.Figure(data=[go.Bar(
                x=cat_totals.index,
                y=cat_totals.values,
                marker_color='#4CAF50'
            )])
            fig.update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show percentages
            for cat, total in cat_totals.items():
                pct = (total / total_spent) * 100
                st.write(f"**{cat}**: ${total:,.2f} ({pct:.1f}%)")
        
        with col2:
            st.subheader("Monthly Trend")
            monthly = st.session_state.expenses.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
            monthly['Period'] = monthly.apply(lambda x: f"{MONTH_NAMES[int(x['Month'])][:3]} {int(x['Year'])}", axis=1)
            
            fig = go.Figure(data=[go.Scatter(
                x=monthly['Period'],
                y=monthly['Amount'],
                mode='lines+markers',
                line=dict(color='#45B7D1', width=3),
                marker=dict(size=10)
            )])
            fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Goals":
    st.header("🎯 Financial Goals & Savings Tracker")
    
    tab1, tab2, tab3 = st.tabs(["💰 Savings Overview", "➕ Manage Goals", "📊 Goal Roadmap"])
    
    with tab1:
        st.subheader("💎 Your Current Financial Status")
        
        # Calculate actual savings from income - expenses
        if not st.session_state.expenses.empty and st.session_state.salary > 0:
            total_income = 0
            if st.session_state.salary_history:
                total_income = sum(st.session_state.salary_history.values())
            else:
                months = len(st.session_state.expenses['Month'].unique())
                total_income = st.session_state.salary * months
            
            total_expenses = st.session_state.expenses['Amount'].sum()
            calculated_savings = max(0, total_income - total_expenses)
        else:
            calculated_savings = 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Your Savings")
            st.metric("Total Accumulated Savings", f"${calculated_savings:,.2f}", "Based on income - expenses")
            st.info("This is calculated from your salary history minus all expenses.")
        
        with col2:
            st.markdown("### 🚨 Emergency Fund")
            emergency_target = st.number_input(
                "Emergency fund target:",
                min_value=0.0,
                value=float(st.session_state.emergency_fund_target),
                step=50.0,
                format="%.2f",
                key="emergency_target_input"
            )
            
            if st.button("Update Emergency Target", type="primary"):
                st.session_state.emergency_fund_target = emergency_target
                st.success(f"✓ Emergency target updated to ${emergency_target:,.2f}")
                st.rerun()
            
            emergency_progress = min(100, (calculated_savings / st.session_state.emergency_fund_target) * 100) if st.session_state.emergency_fund_target > 0 else 0
            st.progress(emergency_progress / 100)
            st.metric("Emergency Fund Status", f"{emergency_progress:.1f}%", 
                     f"${max(0, st.session_state.emergency_fund_target - calculated_savings):,.2f} needed")
        
        st.markdown("---")
        
        # Calculate monthly savings capacity
        if not st.session_state.expenses.empty and st.session_state.salary > 0:
            # Get last 3 months of data properly
            df = st.session_state.expenses.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            three_months_ago = datetime.now() - timedelta(days=90)
            recent_df = df[df['Date'] >= three_months_ago]
            
            if not recent_df.empty:
                # Count actual months in the data
                months_count = len(recent_df['Month'].unique())
                if months_count > 0:
                    recent_spending = recent_df['Amount'].sum() / months_count
                else:
                    recent_spending = recent_df['Amount'].sum() / 3
            else:
                recent_spending = 0
            
            monthly_savings_capacity = max(0, st.session_state.salary - recent_spending)
        else:
            recent_spending = 0
            monthly_savings_capacity = st.session_state.salary * 0.20
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Salary", f"${st.session_state.salary:,.2f}")
        col2.metric("Avg Monthly Spending", f"${recent_spending:,.2f}")
        col3.metric("Monthly Savings Capacity", f"${monthly_savings_capacity:,.2f}")
        
        # Available for goals after emergency fund
        available_for_goals = max(0, calculated_savings - st.session_state.emergency_fund_target)
        
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='margin: 0; color: white;'>💰 Available for Goals</h3>
            <p style='margin: 10px 0;'>
                <strong>Total Savings:</strong> ${calculated_savings:,.2f}<br>
                <strong>Emergency Reserve:</strong> ${st.session_state.emergency_fund_target:,.2f}<br>
                <strong>Available for Goals:</strong> ${available_for_goals:,.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("➕ Add New Goal")
    
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input("Goal Name", "New Laptop")
            goal_amount = st.number_input("Target Amount ($)", min_value=0.0, value=1500.0, step=100.0)
            goal_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        with col2:
            goal_year = st.number_input("Target Year", min_value=2026, max_value=2050, value=2026)
            goal_month = st.selectbox("Target Month", list(range(1, 13)), 
                                     format_func=lambda x: MONTH_NAMES[x])
        
        if st.button("Add Goal", type="primary"):
            if goal_name and goal_amount > 0:
                current_date = datetime.now().year * 12 + datetime.now().month
                target_date = goal_year * 12 + goal_month
                months_until = target_date - current_date
                
                if months_until > 0:
                    goal = {
                        'name': goal_name,
                        'target_amount': goal_amount,
                        'target_year': goal_year,
                        'target_month': goal_month,
                        'months_until_goal': months_until,
                        'monthly_savings_needed': goal_amount / months_until,
                        'priority': goal_priority,
                        'allocated_savings': 0
                    }
                    
                    st.session_state.goals.append(goal)
                    st.success(f"✓ Goal '{goal_name}' added! Need ${goal['monthly_savings_needed']:.2f}/month")
                    st.rerun()
                else:
                    st.error("Target date must be in the future!")
            else:
                st.error("Please enter valid goal details!")
        
        st.markdown("---")
        st.subheader("📋 Your Goals")
        
        if not st.session_state.goals:
            st.info("No goals yet! Add a goal above.")
        else:
            for i, goal in enumerate(st.session_state.goals):
                priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                with st.expander(f"{priority_color.get(goal.get('priority', 'Medium'), '🟡')} {goal['name']} - ${goal['target_amount']:,.2f}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Priority:** {goal.get('priority', 'Medium')}")
                        st.write(f"**Target:** ${goal['target_amount']:,.2f}")
                        st.write(f"**Due:** {MONTH_NAMES[goal['target_month']]} {goal['target_year']}")
                        st.write(f"**Months Remaining:** {goal['months_until_goal']}")
                        st.write(f"**Monthly Need:** ${goal['monthly_savings_needed']:.2f}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{i}"):
                            st.session_state[f'editing_goal_{i}'] = True
                            st.rerun()
                        
                        if st.button("🗑️ Delete", key=f"delete_{i}"):
                            st.session_state.goals.pop(i)
                            st.success(f"✓ Deleted: {goal['name']}")
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get(f'editing_goal_{i}', False):
                        st.markdown("---")
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            new_name = st.text_input("Name", value=goal['name'], key=f"edit_name_{i}")
                            new_amount = st.number_input("Amount", min_value=0.0, value=float(goal['target_amount']), step=100.0, key=f"edit_amount_{i}")
                            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(goal.get('priority', 'Medium')), key=f"edit_priority_{i}")
                        
                        with edit_col2:
                            new_year = st.number_input("Year", min_value=2026, max_value=2050, value=goal['target_year'], key=f"edit_year_{i}")
                            new_month = st.selectbox("Month", list(range(1, 13)), index=goal['target_month']-1, format_func=lambda x: MONTH_NAMES[x], key=f"edit_month_{i}")
                        
                        if st.button("💾 Save", key=f"save_{i}", type="primary"):
                            current_date = datetime.now().year * 12 + datetime.now().month
                            target_date = new_year * 12 + new_month
                            months_until = target_date - current_date
                            
                            if months_until > 0:
                                st.session_state.goals[i] = {
                                    'name': new_name,
                                    'target_amount': new_amount,
                                    'target_year': new_year,
                                    'target_month': new_month,
                                    'months_until_goal': months_until,
                                    'monthly_savings_needed': new_amount / months_until,
                                    'priority': new_priority,
                                    'allocated_savings': goal.get('allocated_savings', 0)
                                }
                                st.session_state[f'editing_goal_{i}'] = False
                                st.success(f"✓ Updated: {new_name}")
                                st.rerun()
                        
                        if st.button("❌ Cancel", key=f"cancel_{i}"):
                            st.session_state[f'editing_goal_{i}'] = False
                            st.rerun()
    
    with tab3:
        st.subheader("📊 Smart Goal Roadmap")
        
        if not st.session_state.goals:
            st.info("No goals yet! Add goals in the 'Manage Goals' tab.")
        else:
            # Calculate monthly savings capacity
            if not st.session_state.expenses.empty and st.session_state.salary > 0:
                # Get last 3 months of data properly
                df = st.session_state.expenses.copy()
                df['Date'] = pd.to_datetime(df['Date'])
                three_months_ago = datetime.now() - timedelta(days=90)
                recent_df = df[df['Date'] >= three_months_ago]
                
                if not recent_df.empty:
                    # Count actual months in the data
                    months_count = len(recent_df['Month'].unique())
                    if months_count > 0:
                        recent_spending = recent_df['Amount'].sum() / months_count
                    else:
                        recent_spending = recent_df['Amount'].sum() / 3
                else:
                    recent_spending = 0
                
                monthly_savings_capacity = max(0, st.session_state.salary - recent_spending)
            else:
                monthly_savings_capacity = st.session_state.salary * 0.20
            
            # Calculate actual savings
            if not st.session_state.expenses.empty and st.session_state.salary > 0:
                total_income = 0
                if st.session_state.salary_history:
                    total_income = sum(st.session_state.salary_history.values())
                else:
                    months = len(st.session_state.expenses['Month'].unique())
                    total_income = st.session_state.salary * months
                
                total_expenses = st.session_state.expenses['Amount'].sum()
                calculated_savings = max(0, total_income - total_expenses)
            else:
                calculated_savings = 0
            
            # Current financial status
            available_for_goals = max(0, calculated_savings - st.session_state.emergency_fund_target)
            emergency_shortfall = max(0, st.session_state.emergency_fund_target - calculated_savings)
            
            st.markdown(f"""
            <div class='info-box'>
                <h3 style='margin: 0; color: white;'>💰 Current Financial Status</h3>
                <p style='margin: 10px 0 5px 0;'><strong>Total Savings:</strong> ${calculated_savings:,.2f}</p>
                <p style='margin: 5px 0;'><strong>Emergency Fund Target:</strong> ${st.session_state.emergency_fund_target:,.2f}</p>
                <p style='margin: 5px 0;'><strong>Emergency Shortfall:</strong> ${emergency_shortfall:,.2f}</p>
                <p style='margin: 5px 0;'><strong>Available for Goals:</strong> ${available_for_goals:,.2f}</p>
                <p style='margin: 5px 0;'><strong>Monthly Savings Capacity:</strong> ${monthly_savings_capacity:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Sort goals by priority and deadline
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            sorted_goals = sorted(st.session_state.goals, 
                                 key=lambda g: (priority_order.get(g.get('priority', 'Medium'), 1), 
                                               g['months_until_goal']))
            
            # Calculate optimal allocation strategy
            st.subheader("🎯 Recommended Goal Achievement Strategy")
            
            # Step 1: Emergency Fund First
            if emergency_shortfall > 0:
                months_for_emergency = int(np.ceil(emergency_shortfall / monthly_savings_capacity)) if monthly_savings_capacity > 0 else 999
                st.markdown(f"""
                <div class='warning-box'>
                    <h4 style='margin: 0; color: white;'>🚨 PRIORITY 1: Complete Emergency Fund</h4>
                    <p style='margin: 10px 0 5px 0;'><strong>Needed:</strong> ${emergency_shortfall:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Time:</strong> {months_for_emergency} months at ${monthly_savings_capacity:,.2f}/month</p>
                    <p style='margin: 5px 0;'><strong>Why:</strong> Always keep ${st.session_state.emergency_fund_target:,.2f} for unexpected expenses!</p>
                </div>
                """, unsafe_allow_html=True)
                
                current_month = 0
                running_savings = calculated_savings
            else:
                st.markdown("""
                <div class='success-box'>
                    <h4 style='margin: 0; color: white;'>✅ Emergency Fund Complete!</h4>
                    <p style='margin: 10px 0 0 0;'>Your emergency fund is fully funded. You can focus on your goals!</p>
                </div>
                """, unsafe_allow_html=True)
                current_month = 0
                running_savings = available_for_goals
            
            st.markdown("---")
            st.subheader("📅 Goal Achievement Timeline")
            
            # Create timeline
            timeline_data = []
            cumulative_months = max(1, months_for_emergency if emergency_shortfall > 0 else 0)
            
            for i, goal in enumerate(sorted_goals, 1):
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                emoji = priority_emoji.get(goal.get('priority', 'Medium'), '🟡')
                
                # Check if current savings cover this goal
                if running_savings >= goal['target_amount']:
                    # Can achieve immediately
                    timeline_data.append({
                        'Step': i,
                        'Goal': f"{emoji} {goal['name']}",
                        'Amount': goal['target_amount'],
                        'Start Month': cumulative_months,
                        'End Month': cumulative_months,
                        'Status': '✅ Achievable Now',
                        'Strategy': f"Use ${goal['target_amount']:,.2f} from savings"
                    })
                    running_savings -= goal['target_amount']
                else:
                    # Need to save
                    still_needed = goal['target_amount'] - running_savings
                    months_needed = int(np.ceil(still_needed / monthly_savings_capacity)) if monthly_savings_capacity > 0 else 999
                    
                    timeline_data.append({
                        'Step': i,
                        'Goal': f"{emoji} {goal['name']}",
                        'Amount': goal['target_amount'],
                        'Start Month': cumulative_months,
                        'End Month': cumulative_months + months_needed,
                        'Status': f'💰 Save {months_needed}mo',
                        'Strategy': f"${running_savings:,.2f} from savings + save ${monthly_savings_capacity:,.2f}/mo for {months_needed} months"
                    })
                    
                    cumulative_months += months_needed
                    running_savings = 0  # Used all savings
            
            # Display timeline
            for item in timeline_data:
                months_range = f"Month {item['Start Month']}" if item['Start Month'] == item['End Month'] else f"Months {item['Start Month']}-{item['End Month']}"
                
                st.markdown(f"""
                <div class='info-box'>
                    <h4 style='margin: 0; color: white;'>Step {item['Step']}: {item['Goal']}</h4>
                    <p style='margin: 10px 0 5px 0;'><strong>Target Amount:</strong> ${item['Amount']:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Timeline:</strong> {months_range}</p>
                    <p style='margin: 5px 0;'><strong>Status:</strong> {item['Status']}</p>
                    <p style='margin: 5px 0;'><strong>Strategy:</strong> {item['Strategy']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary
            st.markdown("---")
            total_goal_amount = sum(g['target_amount'] for g in sorted_goals)
            total_time = cumulative_months
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Goals", len(sorted_goals))
            col2.metric("Total Amount Needed", f"${total_goal_amount:,.2f}")
            col3.metric("Estimated Timeline", f"{total_time} months")
            
            # Recommendations
            st.markdown("---")
            st.subheader("💡 Smart Recommendations")
            
            if monthly_savings_capacity < 100:
                st.warning("⚠️ Your monthly savings capacity is low. Consider reducing expenses or increasing income.")
            
            if emergency_shortfall > 0:
                st.info(f"💡 Focus on building your emergency fund to ${st.session_state.emergency_fund_target:,.2f} before pursuing other goals.")
            
            high_priority_goals = [g for g in sorted_goals if g.get('priority') == 'High']
            if len(high_priority_goals) > 2:
                st.info(f"💡 You have {len(high_priority_goals)} high-priority goals. Consider reducing some to medium priority for better focus.")
            
            st.success("✅ Always maintain your emergency fund even after achieving goals!")

elif page == "🤖 AI Insights":
    st.header("🤖 AI-Powered Insights")
    
    tab1, tab2, tab3 = st.tabs(["🔮 Predictions", "🔍 Anomalies", "💡 Optimizer"])
    
    with tab1:
        st.subheader("AI Spending Predictions")
        
        if len(st.session_state.expenses) < 50:
            st.warning("Need at least 50 expenses for AI predictions!")
        else:
            if st.button("Run AI Predictions", type="primary"):
                try:
                    df = st.session_state.expenses.copy()
                    monthly_data = df.groupby(['Year', 'Month', 'Category'])['Amount'].sum().reset_index()
                    
                    le = LabelEncoder()
                    monthly_data['Category_Encoded'] = le.fit_transform(monthly_data['Category'])
                    
                    X = monthly_data[['Year', 'Month', 'Category_Encoded']]
                    y = monthly_data['Amount']
                    
                    rf = RandomForestRegressor(n_estimators=100, random_state=42)
                    rf.fit(X, y)
                    
                    next_month = datetime.now().month + 1
                    next_year = datetime.now().year
                    if next_month > 12:
                        next_month = 1
                        next_year += 1
                    
                    st.success(f"Predictions for {MONTH_NAMES[next_month]} {next_year}:")
                    
                    predictions = []
                    for cat in CATEGORIES:
                        cat_encoded = le.transform([cat])[0]
                        pred = float(rf.predict([[next_year, next_month, cat_encoded]])[0])
                        predictions.append({'Category': cat, 'Predicted Amount': pred})
                    
                    pred_df = pd.DataFrame(predictions)
                    total_pred = pred_df['Predicted Amount'].sum()
                    
                    # Format for display
                    pred_df['Predicted Amount'] = pred_df['Predicted Amount'].apply(lambda x: f"${x:,.2f}")
                    
                    st.dataframe(pred_df, use_container_width=True, hide_index=True)
                    st.metric("Total Predicted", f"${total_pred:,.2f}")
                    
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
    
    with tab2:
        st.subheader("Anomaly Detection")
        
        if len(st.session_state.expenses) < 30:
            st.warning("Need at least 30 expenses for anomaly detection!")
        else:
            if st.button("Detect Anomalies", type="primary"):
                try:
                    df = st.session_state.expenses.copy()
                    amounts = df['Amount'].values.reshape(-1, 1)
                    
                    iso = IsolationForest(contamination=0.1, random_state=42)
                    predictions = iso.fit_predict(amounts)
                    
                    df['Anomaly'] = predictions
                    anomalies = df[df['Anomaly'] == -1]
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Total Analyzed", len(df))
                    col2.metric("Anomalies Found", len(anomalies))
                    
                    if len(anomalies) > 0:
                        st.warning("Unusual transactions detected:")
                        st.dataframe(anomalies[['Date', 'Category', 'Amount', 'Description']].head(20),
                                   use_container_width=True, hide_index=True)
                    else:
                        st.success("✓ No significant anomalies detected!")
                
                except Exception as e:
                    st.error(f"Detection error: {str(e)}")
    
    with tab3:
        st.subheader("💡 Smart Financial Optimizer & Goal Strategy")
        
        # Calculate current savings
        if not st.session_state.expenses.empty and st.session_state.salary > 0:
            total_income = 0
            if st.session_state.salary_history:
                total_income = sum(st.session_state.salary_history.values())
            else:
                months = len(st.session_state.expenses['Month'].unique())
                total_income = st.session_state.salary * months
            
            total_expenses = st.session_state.expenses['Amount'].sum()
            calculated_savings = max(0, total_income - total_expenses)
            
            # Calculate monthly savings capacity
            df = st.session_state.expenses.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            three_months_ago = datetime.now() - timedelta(days=90)
            recent_df = df[df['Date'] >= three_months_ago]
            
            if not recent_df.empty:
                months_count = len(recent_df['Month'].unique())
                if months_count > 0:
                    recent_spending = recent_df['Amount'].sum() / months_count
                else:
                    recent_spending = recent_df['Amount'].sum() / 3
            else:
                recent_spending = 0
            
            monthly_savings_capacity = max(0, st.session_state.salary - recent_spending)
        else:
            calculated_savings = 0
            recent_spending = 0
            monthly_savings_capacity = st.session_state.salary * 0.20
        
        # Display financial overview
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='margin: 0; color: white;'>💰 Your Financial Status</h3>
            <p style='margin: 10px 0 5px 0;'><strong>Total Savings:</strong> ${calculated_savings:,.2f}</p>
            <p style='margin: 5px 0;'><strong>Emergency Fund Target:</strong> ${st.session_state.emergency_fund_target:,.2f}</p>
            <p style='margin: 5px 0;'><strong>Available for Goals:</strong> ${max(0, calculated_savings - st.session_state.emergency_fund_target):,.2f}</p>
            <p style='margin: 5px 0;'><strong>Monthly Savings Capacity:</strong> ${monthly_savings_capacity:,.2f}</p>
            <p style='margin: 5px 0;'><strong>Avg Monthly Spending:</strong> ${recent_spending:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Option 1: Optimize for a specific goal
        st.subheader("🎯 Option 1: Optimize for Specific Goal")
        
        if not st.session_state.goals:
            st.info("📝 Add goals in the 'Manage Goals' tab to get personalized optimization advice!")
        else:
            goal = st.selectbox("Select Goal to Optimize", 
                               [g['name'] for g in st.session_state.goals],
                               key="optimizer_goal_select")
            
            if st.button("🔍 Analyze This Goal", type="primary"):
                selected_goal = next(g for g in st.session_state.goals if g['name'] == goal)
                
                savings_gap = selected_goal['monthly_savings_needed'] - monthly_savings_capacity
                
                st.markdown(f"""
                <div class='info-box'>
                    <h4 style='margin: 0; color: white;'>📋 Goal Details</h4>
                    <p style='margin: 10px 0 5px 0;'><strong>Goal:</strong> {selected_goal['name']}</p>
                    <p style='margin: 5px 0;'><strong>Target Amount:</strong> ${selected_goal['target_amount']:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Deadline:</strong> {selected_goal['months_until_goal']} months</p>
                    <p style='margin: 5px 0;'><strong>Priority:</strong> {selected_goal.get('priority', 'Medium')}</p>
                    <p style='margin: 5px 0;'><strong>Monthly Savings Needed:</strong> ${selected_goal['monthly_savings_needed']:.2f}</p>
                    <p style='margin: 5px 0;'><strong>Your Current Capacity:</strong> ${monthly_savings_capacity:.2f}/month</p>
                </div>
                """, unsafe_allow_html=True)
                
                if savings_gap > 0:
                    st.markdown(f"""
                    <div class='warning-box'>
                        <h4 style='margin: 0;'>⚠️ Savings Gap: ${savings_gap:.2f}/month</h4>
                        <p style='margin: 10px 0 0 0;'>You need to increase your monthly savings by ${savings_gap:.2f} to reach this goal on time.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("💡 Recommended Actions:")
                    
                    # Category spending analysis
                    if not recent_df.empty:
                        cat_spending = recent_df.groupby('Category')['Amount'].sum() / months_count
                        recommendations = []
                        
                        for cat in cat_spending.sort_values(ascending=False).head(5).index:
                            current = cat_spending[cat]
                            reduction_pct = 0.15  # 15% reduction
                            reduction = current * reduction_pct
                            target = current - reduction
                            
                            recommendations.append({
                                'Category': cat,
                                'Current Monthly': f"${current:.2f}",
                                'Suggested Target': f"${target:.2f}",
                                'Monthly Savings': f"${reduction:.2f}",
                                'Annual Impact': f"${reduction * 12:.2f}"
                            })
                        
                        st.markdown("**📊 Category-by-Category Reduction Plan:**")
                        st.dataframe(pd.DataFrame(recommendations), use_container_width=True, hide_index=True)
                        
                        total_reduction = sum([cat_spending[cat] * 0.15 for cat in cat_spending.sort_values(ascending=False).head(5).index])
                        
                        if total_reduction >= savings_gap:
                            st.success(f"✅ By reducing spending in these top 5 categories by 15%, you'll save ${total_reduction:.2f}/month, which covers your ${savings_gap:.2f} gap!")
                        else:
                            remaining = savings_gap - total_reduction
                            st.warning(f"⚠️ After these reductions (${total_reduction:.2f}), you still need ${remaining:.2f}/month. Consider extending the deadline or finding additional income.")
                else:
                    st.success("✓ Great news! You're already saving enough to reach this goal on time!")
                    ahead_by = monthly_savings_capacity - selected_goal['monthly_savings_needed']
                    months_early = int((selected_goal['target_amount'] / monthly_savings_capacity) * (ahead_by / monthly_savings_capacity))
                    st.info(f"💪 You could potentially reach this goal {max(1, months_early)} month(s) earlier, or allocate ${ahead_by:.2f}/month to other goals!")
        
        st.markdown("---")
        
        # Option 2: Comprehensive strategy for all goals
        st.subheader("🎯 Option 2: Comprehensive Strategy for All Goals")
        
        if not st.session_state.goals:
            st.info("📝 Add goals in the 'Manage Goals' tab to get a comprehensive strategy!")
        elif st.button("📊 Analyze All Goals & Get Complete Strategy", type="primary", key="analyze_all"):
            st.markdown("### 🎯 Complete Financial Goal Strategy")
            
            # Emergency fund analysis
            emergency_shortfall = max(0, st.session_state.emergency_fund_target - calculated_savings)
            
            if emergency_shortfall > 0:
                st.markdown(f"""
                <div class='warning-box'>
                    <h4 style='margin: 0;'>🚨 PRIORITY 1: Emergency Fund</h4>
                    <p style='margin: 10px 0 5px 0;'><strong>Status:</strong> ${calculated_savings:,.2f} / ${st.session_state.emergency_fund_target:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Shortfall:</strong> ${emergency_shortfall:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Time Needed:</strong> {int(np.ceil(emergency_shortfall / monthly_savings_capacity)) if monthly_savings_capacity > 0 else 999} months</p>
                    <p style='margin: 5px 0;'><strong>Why First:</strong> Protect against unexpected expenses before pursuing other goals.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='success-box'>
                    <h4 style='margin: 0;'>✅ Emergency Fund Complete!</h4>
                    <p style='margin: 10px 0 0 0;'>Your emergency fund is fully funded. Ready to focus on goals!</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Analyze all goals
            st.subheader("📋 All Goals Analysis")
            
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            sorted_goals = sorted(st.session_state.goals, 
                                 key=lambda g: (priority_order.get(g.get('priority', 'Medium'), 1), 
                                               g['months_until_goal']))
            
            total_needed_monthly = sum(g['monthly_savings_needed'] for g in st.session_state.goals)
            
            for i, g in enumerate(sorted_goals, 1):
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(g.get('priority', 'Medium'), '🟡')
                
                can_afford = monthly_savings_capacity >= g['monthly_savings_needed']
                status_emoji = "✅" if can_afford else "⚠️"
                
                st.markdown(f"""
                <div class='{"success-box" if can_afford else "warning-box"}'>
                    <h4 style='margin: 0;'>{status_emoji} Goal #{i}: {g['name']} {priority_emoji}</h4>
                    <p style='margin: 10px 0 5px 0;'><strong>Target:</strong> ${g['target_amount']:,.2f}</p>
                    <p style='margin: 5px 0;'><strong>Deadline:</strong> {g['months_until_goal']} months</p>
                    <p style='margin: 5px 0;'><strong>Monthly Savings Needed:</strong> ${g['monthly_savings_needed']:.2f}</p>
                    <p style='margin: 5px 0;'><strong>Status:</strong> {"Can afford with current capacity" if can_afford else f"Need ${g['monthly_savings_needed'] - monthly_savings_capacity:.2f} more per month"}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Overall strategy
            st.subheader("💡 Recommended Overall Strategy")
            
            if total_needed_monthly <= monthly_savings_capacity:
                st.success(f"""
                ✅ **Great news!** Your monthly savings capacity (${monthly_savings_capacity:.2f}) can cover all goals combined (${total_needed_monthly:.2f}/month).
                
                **Recommended approach:**
                1. Maintain emergency fund at ${st.session_state.emergency_fund_target:,.2f}
                2. Follow the sequential timeline in 'Goal Roadmap' tab
                3. Focus on high-priority goals first
                4. As you complete each goal, redirect funds to the next
                """)
            else:
                gap = total_needed_monthly - monthly_savings_capacity
                st.warning(f"""
                ⚠️ **Challenge Detected:** Total monthly needs (${total_needed_monthly:.2f}) exceed your capacity (${monthly_savings_capacity:.2f}) by ${gap:.2f}/month.
                
                **Recommended strategies:**
                """)
                
                st.markdown("**Option A: Sequential Approach** (Recommended)")
                st.info("""
                Focus on ONE goal at a time in priority order:
                - Complete high-priority goals first
                - Once achieved, redirect full capacity to next goal
                - This guarantees success on important goals
                - Timeline will be longer but more achievable
                """)
                
                st.markdown("**Option B: Parallel Approach with Trade-offs**")
                st.info("""
                Work on multiple goals simultaneously:
                - Extend deadlines for some goals
                - Accept slower progress on lower-priority items
                - Requires more discipline and tracking
                """)
                
                st.markdown("**Option C: Increase Capacity**")
                
                # Show spending reduction opportunities
                if not recent_df.empty:
                    cat_spending = recent_df.groupby('Category')['Amount'].sum() / months_count
                    st.info(f"""
                    **Reduce spending by ${gap:.2f}/month through:**
                    - Top 3 spending categories: {', '.join(cat_spending.sort_values(ascending=False).head(3).index.tolist())}
                    - Consider 15-20% reduction across these categories
                    - OR seek additional income sources (side gig, raise, etc.)
                    """)
            
            st.markdown("---")
            
            # Action items
            st.subheader("✅ Next Steps")
            st.markdown("""
            1. **Review the Goal Roadmap tab** for sequential timeline
            2. **Track spending weekly** to stay on target
            3. **Adjust priorities** if circumstances change
            4. **Celebrate milestones** to stay motivated
            5. **Review strategy monthly** and adjust as needed
            """)
        
        elif len(st.session_state.goals) > 0:
            st.info(f"💡 You have {len(st.session_state.goals)} active goal(s). Click above to get a comprehensive strategy for managing all of them together!")

# Footer
st.markdown("---")

# Display Bzwen Team branding with logo
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("<p style='text-align: center; color: #888;'>💰 Smart Budget Planner | AI-Powered Finance Manager</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 14px; margin: 0;'>Powered by <strong>Bzwen Team</strong></p>", unsafe_allow_html=True)
    try:
        st.image("BzweenLogo.svg", width=120)
    except:
        st.markdown("<p style='text-align: center; color: #888; font-size: 12px;'>🚀 Bzwen Team</p>", unsafe_allow_html=True)
