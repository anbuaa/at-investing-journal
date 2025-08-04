
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import locale
from io import StringIO

# Configure page
st.set_page_config(
    page_title="Personal Investment Journal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for themes
def load_css():
    return """
    <style>
    .metric-card {
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .positive { color: #28a745; }
    .negative { color: #dc3545; }

    .stMetric > div > div > div > div {
        color: var(--text-color);
    }

    /* Dark theme variables */
    [data-theme="dark"] {
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --text-color: #fafafa;
        --border-color: #464747;
    }

    /* Light theme variables */
    [data-theme="light"] {
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #262730;
        --border-color: #e0e0e0;
    }
    </style>
    """

# Initialize session state
def init_session_state():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    if 'investment_data' not in st.session_state:
        # Sample data with INR currency
        st.session_state.investment_data = [
            {
                'Date': '2024-01-15',
                'Type': 'Stock',
                'Symbol': 'TCS.NS',
                'Name': 'Tata Consultancy Services',
                'Action': 'Buy',
                'Quantity': 10,
                'Price': 3500.00,
                'Total_Value': 35000.00,
                'Rationale': 'Strong Q3 results and digital transformation demand',
                'Outcome_Notes': 'Stock up 8% after good quarterly results',
                'Current_Price': 3780.00,
                'Unrealized_PnL': 2800.00
            },
            {
                'Date': '2024-02-10',
                'Type': 'Mutual Fund',
                'Symbol': 'SBI-BLUECHIP',
                'Name': 'SBI Bluechip Fund',
                'Action': 'Buy',
                'Quantity': 100,
                'Price': 850.00,
                'Total_Value': 85000.00,
                'Rationale': 'Diversified large cap exposure for long term wealth creation',
                'Outcome_Notes': 'Steady performance as expected',
                'Current_Price': 895.50,
                'Unrealized_PnL': 4550.00
            },
            {
                'Date': '2024-03-05',
                'Type': 'Stock',
                'Symbol': 'INFY.NS',
                'Name': 'Infosys Limited',
                'Action': 'Sell',
                'Quantity': 20,
                'Price': 1450.00,
                'Total_Value': 29000.00,
                'Rationale': 'Booking profits after 25% gain, concerned about margin pressure',
                'Outcome_Notes': 'Good exit timing, stock consolidated afterwards',
                'Current_Price': 1420.00,
                'Unrealized_PnL': 0.00
            }
        ]

# Format currency in INR
def format_inr(amount):
    """Format amount in Indian Rupee format"""
    if amount == 0:
        return "₹0.00"

    # Handle negative amounts
    is_negative = amount < 0
    amount = abs(amount)

    # Format with Indian numbering system
    amount_str = f"{amount:,.2f}"

    # Convert to Indian numbering (lakhs and crores)
    parts = amount_str.split('.')
    integer_part = parts[0].replace(',', '')
    decimal_part = parts[1]

    # Format according to Indian system
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        formatted = last_three
        while len(remaining) > 2:
            formatted = remaining[-2:] + ',' + formatted
            remaining = remaining[:-2]

        if remaining:
            formatted = remaining + ',' + formatted

        result = f"₹{formatted}.{decimal_part}"
    else:
        result = f"₹{amount_str}"

    return f"-{result}" if is_negative else result

# Theme toggle
def theme_toggle():
    st.sidebar.markdown("### 🎨 Theme Settings")

    # Theme selector
    current_theme = st.session_state.get('theme', 'light')
    theme_options = {'Light Mode 🌞': 'light', 'Dark Mode 🌙': 'dark'}

    selected_theme_label = st.sidebar.selectbox(
        "Choose Theme:",
        options=list(theme_options.keys()),
        index=0 if current_theme == 'light' else 1
    )

    selected_theme = theme_options[selected_theme_label]

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

# Dashboard metrics
def display_dashboard():
    st.header("📊 Investment Dashboard")

    df = pd.DataFrame(st.session_state.investment_data)

    # Calculate metrics
    total_investment = df[df['Action'] == 'Buy']['Total_Value'].sum()
    current_value = sum([
        row['Quantity'] * row['Current_Price'] 
        for _, row in df[df['Action'] == 'Buy'].iterrows()
    ])
    total_pnl = df['Unrealized_PnL'].sum()
    pnl_percentage = (total_pnl / total_investment * 100) if total_investment > 0 else 0

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Investment",
            format_inr(total_investment),
            help="Total amount invested"
        )

    with col2:
        st.metric(
            "Current Value",
            format_inr(current_value),
            help="Current market value of holdings"
        )

    with col3:
        st.metric(
            "Unrealized P&L",
            format_inr(total_pnl),
            delta=f"{pnl_percentage:.2f}%",
            help="Profit/Loss on current holdings"
        )

    with col4:
        best_performer = df.loc[df['Unrealized_PnL'].idxmax()] if not df.empty else None
        if best_performer is not None:
            st.metric(
                "Best Performer",
                best_performer['Symbol'],
                delta=format_inr(best_performer['Unrealized_PnL'])
            )

    # Portfolio allocation chart
    if not df.empty:
        st.subheader("Portfolio Allocation")

        # Create allocation by type
        allocation_data = df[df['Action'] == 'Buy'].groupby('Type').agg({
            'Total_Value': 'sum'
        }).reset_index()

        if not allocation_data.empty:
            fig = px.pie(
                allocation_data,
                values='Total_Value',
                names='Type',
                title="Investment Allocation by Type"
            )

            # Update colors based on theme
            if st.session_state.theme == 'dark':
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )

            st.plotly_chart(fig, use_container_width=True)

        # Recent transactions
        st.subheader("Recent Transactions")
        recent_df = df.head(5)[['Date', 'Symbol', 'Action', 'Quantity', 'Price', 'Rationale']]
        st.dataframe(recent_df, use_container_width=True)

# Add transaction form
def add_transaction():
    st.header("➕ Add New Transaction")

    with st.form("transaction_form"):
        col1, col2 = st.columns(2)

        with col1:
            trans_date = st.date_input("Date", value=date.today())
            investment_type = st.selectbox(
                "Investment Type",
                ["Stock", "Mutual Fund", "ETF", "Bond", "REIT"]
            )
            symbol = st.text_input("Symbol/Code", placeholder="e.g., TCS.NS, SBIN.NS")
            action = st.selectbox("Action", ["Buy", "Sell", "Dividend"])

        with col2:
            name = st.text_input("Investment Name", placeholder="e.g., Tata Consultancy Services")
            quantity = st.number_input("Quantity", min_value=0.0, step=1.0)
            price = st.number_input("Price per Unit (₹)", min_value=0.0, step=0.01)
            total_value = quantity * price
            st.metric("Total Value", format_inr(total_value))

        rationale = st.text_area(
            "Investment Rationale",
            placeholder="Why are you making this investment decision?"
        )

        outcome_notes = st.text_area(
            "Outcome Notes (Optional)",
            placeholder="Add notes about the outcome later"
        )

        submitted = st.form_submit_button("Add Transaction", type="primary")

        if submitted:
            if symbol and name and quantity > 0 and price > 0:
                new_transaction = {
                    'Date': trans_date.strftime('%Y-%m-%d'),
                    'Type': investment_type,
                    'Symbol': symbol.upper(),
                    'Name': name,
                    'Action': action,
                    'Quantity': quantity,
                    'Price': price,
                    'Total_Value': total_value,
                    'Rationale': rationale,
                    'Outcome_Notes': outcome_notes,
                    'Current_Price': price,  # Initially same as purchase price
                    'Unrealized_PnL': 0.0 if action == 'Sell' else 0.0
                }

                st.session_state.investment_data.append(new_transaction)
                st.success("Transaction added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# Portfolio review
def portfolio_review():
    st.header("📈 Portfolio Review")

    df = pd.DataFrame(st.session_state.investment_data)

    if df.empty:
        st.info("No transactions recorded yet. Add some transactions to see your portfolio.")
        return

    # Create portfolio summary (only buy transactions)
    portfolio_df = df[df['Action'] == 'Buy'].copy()

    if not portfolio_df.empty:
        # Group by symbol to handle multiple purchases
        portfolio_summary = portfolio_df.groupby(['Symbol', 'Name', 'Type']).agg({
            'Quantity': 'sum',
            'Total_Value': 'sum',
            'Current_Price': 'last',  # Take the latest price
            'Unrealized_PnL': 'sum'
        }).reset_index()

        # Calculate average cost
        portfolio_summary['Avg_Cost'] = portfolio_summary['Total_Value'] / portfolio_summary['Quantity']
        portfolio_summary['Market_Value'] = portfolio_summary['Quantity'] * portfolio_summary['Current_Price']
        portfolio_summary['PnL_Percent'] = ((portfolio_summary['Market_Value'] - portfolio_summary['Total_Value']) / portfolio_summary['Total_Value'] * 100)

        # Format currency columns for display
        display_df = portfolio_summary.copy()
        for col in ['Avg_Cost', 'Current_Price', 'Market_Value', 'Total_Value', 'Unrealized_PnL']:
            display_df[col] = display_df[col].apply(format_inr)
        display_df['PnL_Percent'] = display_df['PnL_Percent'].apply(lambda x: f"{x:.2f}%")

        st.subheader("Current Holdings")
        st.dataframe(display_df, use_container_width=True)

        # Performance analysis
        st.subheader("Performance Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Top performers
            top_performers = portfolio_summary.nlargest(3, 'Unrealized_PnL')
            st.markdown("**🏆 Top Performers**")
            for _, row in top_performers.iterrows():
                st.write(f"• {row['Symbol']}: {format_inr(row['Unrealized_PnL'])} ({row['PnL_Percent']:.1f}%)")

        with col2:
            # Bottom performers
            bottom_performers = portfolio_summary.nsmallest(3, 'Unrealized_PnL')
            st.markdown("**📉 Need Attention**")
            for _, row in bottom_performers.iterrows():
                st.write(f"• {row['Symbol']}: {format_inr(row['Unrealized_PnL'])} ({row['PnL_Percent']:.1f}%)")

# Analysis section
def investment_analysis():
    st.header("🔍 Investment Analysis")

    df = pd.DataFrame(st.session_state.investment_data)

    if df.empty:
        st.info("No data available for analysis.")
        return

    # Rationale vs Outcome Analysis
    st.subheader("💡 Learning from Decisions")

    for _, row in df.iterrows():
        with st.expander(f"{row['Symbol']} - {row['Action']} on {row['Date']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Investment Rationale:**")
                st.write(row['Rationale'])
                st.markdown("**Details:**")
                st.write(f"• Type: {row['Type']}")
                st.write(f"• Quantity: {row['Quantity']}")
                st.write(f"• Price: {format_inr(row['Price'])}")
                st.write(f"• Total Value: {format_inr(row['Total_Value'])}")

            with col2:
                st.markdown("**Outcome & Learnings:**")
                if row['Outcome_Notes']:
                    st.write(row['Outcome_Notes'])
                else:
                    st.write("*No outcome notes added yet*")

                if row['Action'] == 'Buy' and row['Unrealized_PnL'] != 0:
                    pnl_color = "green" if row['Unrealized_PnL'] > 0 else "red"
                    st.markdown(f"**Current P&L:** <span style='color:{pnl_color}'>{format_inr(row['Unrealized_PnL'])}</span>", unsafe_allow_html=True)

# Data management
def data_management():
    st.header("💾 Data Management")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📥 Import Data")

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file with your investment data"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)

                # Validate required columns
                required_cols = ['Date', 'Type', 'Symbol', 'Name', 'Action', 'Quantity', 'Price', 'Total_Value', 'Rationale']
                if all(col in df.columns for col in required_cols):
                    st.session_state.investment_data = df.to_dict('records')
                    st.success(f"Successfully imported {len(df)} transactions!")
                    st.rerun()
                else:
                    st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

        # Load sample data
        if st.button("Load Sample Data"):
            init_session_state()
            st.success("Sample data loaded!")
            st.rerun()

    with col2:
        st.subheader("📤 Export Data")

        if st.session_state.investment_data:
            df = pd.DataFrame(st.session_state.investment_data)

            # Prepare CSV
            csv = df.to_csv(index=False)

            st.download_button(
                label="📁 Download as CSV",
                data=csv,
                file_name=f"investment_journal_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
        else:
            st.info("No data to export. Add some transactions first.")

        # Clear data option
        st.subheader("⚠️ Clear Data")
        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("I understand this will delete all my data"):
                st.session_state.investment_data = []
                st.success("All data cleared!")
                st.rerun()

# Main app
def main():
    # Initialize session state
    init_session_state()

    # Apply CSS
    st.markdown(load_css(), unsafe_allow_html=True)

    # Apply theme
    theme_class = f'data-theme="{st.session_state.theme}"'
    st.markdown(f'<div {theme_class}>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("🏦 Investment Journal")
    st.sidebar.markdown("---")

    # Theme toggle
    theme_toggle()

    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["📊 Dashboard", "➕ Add Transaction", "📈 Portfolio Review", "🔍 Analysis", "💾 Data Management"]
    )

    # Currency info
    st.sidebar.info("💰 All amounts are in Indian Rupees (₹)")

    # Main content
    if page == "📊 Dashboard":
        display_dashboard()
    elif page == "➕ Add Transaction":
        add_transaction()
    elif page == "📈 Portfolio Review":
        portfolio_review()
    elif page == "🔍 Analysis":
        investment_analysis()
    elif page == "💾 Data Management":
        data_management()

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit | "
        f"Theme: {'🌙 Dark' if st.session_state.theme == 'dark' else '🌞 Light'}"
    )

if __name__ == "__main__":
    main()
