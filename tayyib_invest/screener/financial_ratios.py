from tayyib_invest.screener.business_sector import BusinessSectorValidator


class FinancialRatioScreener:
    def __init__(self, financials: dict) -> None:
        self.financials = financials["financials"]
        self.balance_sheet = financials["balance_sheet"]
        self.info = financials["info"]

        self.debt_threshold = 30
        self.cash_threshold = 30
        self.non_halal_income_threshold = 5
        self.liquidity_threshold = 70

    @staticmethod
    def _calculate_ratio(numerator: float, denominator: float) -> float:
        """Utility method to calculate ratio safely."""
        return (numerator / denominator * 100) if denominator > 0 else 0

    def income_non_sharia_compliant_ratio(self) -> bool:
        # earnings from equity interest maybe ?

        sector_validator = BusinessSectorValidator(self.info)
        if not sector_validator.is_valid_sector():
            print("This business is in a haram sector.")
            return False

        total_revenue = self.financials.get("Total Revenue", 0)
        total_non_compliant_income = self.financials.get("Interest Income", 0)

        impermissible_income_ratio = self._calculate_ratio(total_non_compliant_income, total_revenue)

        if impermissible_income_ratio > self.non_halal_income_threshold:
            print(f"Not Halal. Impermissible income ratio is {impermissible_income_ratio:.2f}%, which exceeds 5%.")
            return False

        return True

    def debt_cap_ratio(self) -> bool:
        """Calculate the debt-to-market cap ratio and check compliance."""
        total_debt = self.balance_sheet.get("Total Debt", 0)
        total_market_cap = self.info.get("marketCap", 0)

        debt_to_cap_ratio = self._calculate_ratio(total_debt, total_market_cap)

        if debt_to_cap_ratio > self.debt_threshold:
            print(f"Not Halal. Debt-to-market cap ratio is {debt_to_cap_ratio:.2f}%, which exceeds 30%")
            return False

        return True

    def cash_cap_ratio(self) -> bool:
        """Calculate the cash-to-market cap ratio and check compliance."""
        cash_and_equivalents = self.balance_sheet.get("Cash Cash Equivalents And Short Term Investments", 0)
        total_market_cap = self.info.get("marketCap", 0)

        cash_to_cap_ratio = self._calculate_ratio(cash_and_equivalents, total_market_cap)

        if cash_to_cap_ratio > self.cash_threshold:
            print(f"Not Halal. Cash-to-market cap ratio is {cash_to_cap_ratio:.2f}%, which exceeds 30%")
            return False

        return True

    def liquidity_ratio(self) -> bool:
        """Calculate the liquidity ratio and check compliance."""
        cash_and_equivalents = self.balance_sheet.get("Cash Cash Equivalents And Short Term Investments", 0)
        accounts_receivable = self.balance_sheet.get("Accounts Receivable", 0)
        total_market_cap = self.info.get("marketCap", 0)

        cash_and_receivable = cash_and_equivalents + accounts_receivable
        liquidity_ratio = self._calculate_ratio(cash_and_receivable, total_market_cap)

        if liquidity_ratio > self.liquidity_threshold:
            print(f"Not Halal. Liquidity ratio is {liquidity_ratio:.2f}%, which exceeds 70%")
            return False

        return True
