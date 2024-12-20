from unittest.mock import Mock, patch

from tayyib_invest.backend.screener.financial_ratios import FinancialRatioScreener


def test_income_non_sharia_compliant_ratio_compliant(screener: FinancialRatioScreener) -> None:
    """Test income_non_sharia_compliant_ratio compliant method."""

    is_compliant, ratio = screener.income_non_sharia_compliant_ratio()
    assert is_compliant is True
    assert ratio == 3.0


def test_income_non_sharia_compliant_ratio_exceeds_non_compliant(
    financials: dict,
) -> None:
    """Test income_non_sharia_compliant_ratio non-compliant method."""

    data = financials.copy()
    data["financials"]["Interest Income"] = 40000
    data["financials"]["Interest Expense"] = 20000
    screener = FinancialRatioScreener(data)

    is_compliant, ratio = screener.income_non_sharia_compliant_ratio()
    assert is_compliant is False
    assert ratio == 6.0


@patch("tayyib_invest.backend.screener.financial_ratios.BusinessActivityValidator")
def test_income_non_sharia_compliant_ratio_invalid_business(
    mock: Mock, screener: FinancialRatioScreener
) -> None:
    """Test income_non_sharia_compliant_ratio invalid business method."""

    mock.return_value.is_valid_business_activity.return_value = False
    is_compliant, ratio = screener.income_non_sharia_compliant_ratio()
    assert is_compliant is False
    assert ratio == 100.0


def test_debt_cap_ratio_compliant(screener: FinancialRatioScreener) -> None:
    """Test debt_cap_ratio_compliant method."""

    is_compliant, ratio = screener.debt_cap_ratio()
    assert is_compliant is True
    assert ratio == 25.0


def test_debt_cap_ratio_non_compliant(financials: dict) -> None:
    """Test debt_cap_ratio non-compliant method."""

    data = financials.copy()
    data["balance_sheet"]["Total Debt"] = 400000
    screener = FinancialRatioScreener(data)
    is_compliant, ratio = screener.debt_cap_ratio()
    assert is_compliant is False
    assert ratio == 40.0


def test_cash_cap_ratio_compliant(screener: FinancialRatioScreener) -> None:
    """Test cash_cap_ratio compliant method."""
    is_compliant, ratio = screener.cash_cap_ratio()
    assert is_compliant is True
    assert ratio == 25.0


def test_cash_cap_ratio_non_compliant(financials: dict) -> None:
    """Test cash_cap_ratio non-compliant method."""
    data = financials.copy()
    data["balance_sheet"]["Cash And Cash Equivalents"] = 250000
    data["balance_sheet"]["Other Short Term Investments"] = 100000
    screener = FinancialRatioScreener(data)
    is_compliant, ratio = screener.cash_cap_ratio()
    assert is_compliant is False
    assert ratio == 35.0


def test_liquidity_ratio_compliant(screener: FinancialRatioScreener) -> None:
    """Test liquidity_ratio compliant method."""

    is_compliant, ratio = screener.liquidity_ratio()
    assert is_compliant is True
    assert ratio == 35.0


def test_liquidity_ratio_non_compliant(financials: dict) -> None:
    """Test liquidity_ratio non-compliant method."""

    data = financials.copy()
    data["balance_sheet"]["Cash Cash Equivalents And Short Term Investments"] = 600000
    data["balance_sheet"]["Accounts Receivable"] = 200000
    screener = FinancialRatioScreener(data)
    is_compliant, ratio = screener.liquidity_ratio()
    assert is_compliant is False
    assert ratio == 80.0
