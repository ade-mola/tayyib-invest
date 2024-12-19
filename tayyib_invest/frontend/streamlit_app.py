import requests
import streamlit as st


# Configuration
API_URL = "https://tayyib-invest.vercel.app//v1"
st.set_page_config(page_title="Tayyib Invest - Halal Stock Screener", layout="centered")

# Initialize session state variables
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = None
if "compliance" not in st.session_state:
    st.session_state.compliance = None

# App Header
st.title("Tayyib Invest - Halal Stock Screener")
st.markdown("""
This app helps you find Shariah-compliant stocks based on financial criteria.
Search for stock/company below to check compliance.
""")


# Functions
def search_stocks() -> None:
    """
    Search for stocks based on user input and update session state.
    """
    query = st.session_state.search_query.strip()
    if query:
        try:
            response = requests.post(f"{API_URL}/search", json={"query": query}, timeout=20)
            if response.status_code == 200:
                results = response.json().get("results", [])
                st.session_state.search_results = [
                    {"name": result["name"], "symbol": result["symbol"]} for result in results
                ]
            else:
                st.session_state.search_results = []
                st.error("Error fetching search results.")
        except requests.exceptions.RequestException as e:
            st.session_state.search_results = []
            st.error(f"An error occurred while fetching search results: {e}")
    else:
        st.session_state.search_results = []


def validate_stock_compliance(symbol: str) -> None:
    """
    Validate whether the selected stock is Shariah-compliant.
    """
    if symbol:
        try:
            response = requests.post(
                f"{API_URL}/validate_halal_stock", json={"ticker": symbol}, timeout=20
            )
            if response.status_code == 200:
                st.session_state.compliance = response.json().get("compliance", {})
            else:
                st.session_state.compliance = None
                st.error("Error validating stock compliance.")
        except requests.exceptions.RequestException as e:
            st.session_state.compliance = None
            st.error(f"An error occurred while validating stock: {e}")


def display_compliance_results(compliance: dict) -> None:
    """
    Display the stock compliance results in a user-friendly format.
    """
    if not compliance:
        st.error("No compliance data available.")
        return

    # Display overall status
    st.subheader("Compliance Status")
    status = compliance.get("status", "Unknown")
    reason = compliance.get("reason", "No reason provided.")
    st.write(f"**Status:** {status}")
    st.write(f"**Reason:** {reason}")

    # Display detailed compliance breakdown
    details = compliance.get("details", {})
    if details:
        st.subheader("Detailed Compliance Breakdown")
        for key, value in details.items():
            if isinstance(value, list) and len(value) == 2:
                is_valid = "✅" if value[0] else "❌"
                st.write(
                    f"- **{key.replace('_', ' ').capitalize()}**: {is_valid} (Value: {value[1]})"
                )
            else:
                is_valid = "✅" if value else "❌"
                st.write(f"- **{key.replace('_', ' ').capitalize()}**: {is_valid}")


# Input Section
st.header("Search for Stock/Company")
col1, col2 = st.columns(2)

with col1:
    st.text_input(
        "Enter company name or ticker:",
        key="search_query",
        on_change=search_stocks,
    )

with col2:
    if st.session_state.search_results:
        names = [result["name"] for result in st.session_state.search_results]
        selected_name = st.selectbox("Select a company/stock:", names)

        if selected_name:
            st.session_state.selected_symbol = next(
                (
                    result["symbol"]
                    for result in st.session_state.search_results
                    if result["name"] == selected_name
                ),
                None,
            )

            # Validate stock compliance
            validate_stock_compliance(st.session_state.selected_symbol)

# Compliance Results Section
if st.session_state.compliance is not None:
    st.header("Stock Halal Compliance")
    display_compliance_results(st.session_state.compliance)
