from tayyib_invest.backend.screener.business_activity import BusinessActivityValidator


class FinancialRatioScreener:
    def __init__(self, financials: dict) -> None:
        """Initialize with financial data."""
        self.financials = financials["financials"]
        self.balance_sheet = financials["balance_sheet"]
        self.info = financials["info"]
        self.total_market_cap = self.info.get("marketCap", 0)

        self.debt_threshold = 30
        self.cash_threshold = 30
        self.non_halal_income_threshold = 5
        self.liquidity_threshold = 70

    @staticmethod
    def _calculate_ratio(numerator: float, denominator: float) -> float:
        """Utility method to calculate ratio"""
        return round((numerator / denominator * 100), 2) if denominator > 0 else 0

    def income_non_sharia_compliant_ratio(self) -> tuple[bool, float]:
        """Calculate the income non-Sharia compliant ratio and check compliance."""
        business_validator = BusinessActivityValidator(self.info)
        if not business_validator.is_valid_business_activity():
            print("This business is in a haram sector/industry.")
            return False, 100.0

        total_revenue = self.financials.get("Total Revenue", 0)
        non_compliant_income_sources = [
            self.financials.get("Interest Income", 0),
            self.financials.get("Interest Expense", 0),
        ]
        total_non_compliant_income = sum(non_compliant_income_sources)

        impermissible_income_ratio = self._calculate_ratio(
            total_non_compliant_income, total_revenue
        )

        if impermissible_income_ratio > self.non_halal_income_threshold:
            print(
                f"Not Halal. Impermissible income ratio is {impermissible_income_ratio:.2f}%, which exceeds 5%."
            )
            return False, impermissible_income_ratio

        return True, impermissible_income_ratio

    def debt_cap_ratio(self) -> tuple[bool, float]:
        """Calculate the debt-to-market cap ratio and check compliance."""
        total_debt = self.balance_sheet.get("Total Debt", 0)
        total_market_cap = self.info.get("marketCap", 0)

        debt_to_cap_ratio = self._calculate_ratio(total_debt, total_market_cap)

        if debt_to_cap_ratio > self.debt_threshold:
            print(
                f"Not Halal. Debt-to-market cap ratio is {debt_to_cap_ratio:.2f}%, which exceeds 30%"
            )
            return False, debt_to_cap_ratio

        return True, debt_to_cap_ratio

    def cash_cap_ratio(self) -> tuple[bool, float]:
        """Calculate the cash-to-market cap ratio and check compliance."""
        cash = self.balance_sheet.get("Cash And Cash Equivalents", 0)
        short_term_investments = self.balance_sheet.get("Other Short Term Investments", 0)

        cash_and_investments = cash + short_term_investments

        cash_to_cap_ratio = self._calculate_ratio(cash_and_investments, self.total_market_cap)

        if cash_to_cap_ratio > self.cash_threshold:
            print(
                f"Not Halal. Cash-to-market cap ratio is {cash_to_cap_ratio:.2f}%, which exceeds 30%"
            )
            return False, cash_to_cap_ratio

        return True, cash_to_cap_ratio

    def liquidity_ratio(self) -> tuple[bool, float]:
        """Calculate the liquidity ratio and check compliance."""
        cash_and_equivalents = self.balance_sheet.get(
            "Cash Cash Equivalents And Short Term Investments", 0
        )
        accounts_receivable = self.balance_sheet.get("Accounts Receivable", 0)

        cash_and_receivable = cash_and_equivalents + accounts_receivable
        liquidity_ratio = self._calculate_ratio(cash_and_receivable, self.total_market_cap)

        if liquidity_ratio > self.liquidity_threshold:
            print(f"Not Halal. Liquidity ratio is {liquidity_ratio:.2f}%, which exceeds 70%")
            return False, liquidity_ratio

        return True, liquidity_ratio
