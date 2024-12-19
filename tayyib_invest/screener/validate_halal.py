from fastapi import HTTPException

from ..company_info.company_financials import CompanyFinancials
from ..screener.financial_ratios import FinancialRatioScreener
from .business_sector import BusinessSectorValidator


class ValidateHalalStock:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    async def check_halal(self) -> dict:
        """Check if the stock is Halal based on screening factors."""
        try:
            financials = await CompanyFinancials(self.ticker).get_financials()
            financial_ratios = FinancialRatioScreener(financials)

            business_sector = BusinessSectorValidator(financials["info"])

            validation_methods = [
                business_sector.is_valid_sector,
                financial_ratios.income_non_sharia_compliant_ratio,
                financial_ratios.debt_cap_ratio,
                financial_ratios.cash_cap_ratio,
                financial_ratios.liquidity_ratio,
            ]

            # Check all criteria and collect results
            results = {method.__name__: method() for method in validation_methods}

            if all(results.values()):
                return {"status": "Halal", "reason": "Stock is Shariah compliance."}

            return {
                "status": "Not Halal",
                "reason": "One or more financial criteria are not met.",
                "details": results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
