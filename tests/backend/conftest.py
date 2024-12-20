from datetime import datetime

import pandas as pd
import pytest

from tayyib_invest.backend.screener.financial_ratios import FinancialRatioScreener
from tayyib_invest.backend.screener.validate_halal import ValidateHalalStock


@pytest.fixture
def financials() -> dict:
    return {
        "financials": pd.Series(
            {
                "Total Revenue": 1000000,
                "Interest Income": 20000,
                "Interest Expense": 10000,
            },
            name=datetime(2024, 1, 1),
        ),
        "balance_sheet": pd.Series(
            {
                "Total Debt": 250000,
                "Cash And Cash Equivalents": 200000,
                "Other Short Term Investments": 50000,
                "Cash Cash Equivalents And Short Term Investments": 250000,
                "Accounts Receivable": 100000,
            },
            name=datetime(2024, 1, 1),
        ),
        "info": {
            "marketCap": 1000000,
            "sector": "Technology",
            "industry": "Technology",
            "longName": "Test Company Inc.",
        },
    }


@pytest.fixture
def validator() -> ValidateHalalStock:
    return ValidateHalalStock("TEST")


@pytest.fixture
def screener(financials: dict) -> FinancialRatioScreener:
    return FinancialRatioScreener(financials)
