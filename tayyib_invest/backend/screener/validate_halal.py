from fastapi import HTTPException
from groq import Groq

from tayyib_invest.backend.company_info.company_financials import CompanyFinancials
from tayyib_invest.backend.screener.business_activity import BusinessActivityValidator
from tayyib_invest.backend.screener.financial_ratios import FinancialRatioScreener
from tayyib_invest.config import GROQ_API_KEY


class ValidateHalalStock:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.financials = CompanyFinancials(self.ticker)

    async def _validation_methods(self) -> tuple[dict, float]:
        financials = await self.financials.get_financials()
        financial_ratios = FinancialRatioScreener(financials)
        business_activity = BusinessActivityValidator(financials["info"])

        validation_methods = {
            "is_valid_business_activity": business_activity.is_valid_business_activity,
            "income_non_sharia_compliant_ratio": financial_ratios.income_non_sharia_compliant_ratio,
            "debt_cap_ratio": financial_ratios.debt_cap_ratio,
            "cash_cap_ratio": financial_ratios.cash_cap_ratio,
            "liquidity_ratio": financial_ratios.liquidity_ratio,
        }

        results = {name: method() for name, method in validation_methods.items()}
        return results, financials["info"].get("marketCap", 0.0)

    async def check_halal(self) -> dict:
        """Check if the stock is Halal based on screening factors."""
        try:
            results, _ = await self._validation_methods()

            all_criteria = [
                results.get("is_valid_business_activity", False),
                results["debt_cap_ratio"][0],
                results["cash_cap_ratio"][0],
                results["liquidity_ratio"][0],
                results["income_non_sharia_compliant_ratio"][0],
            ]

            status = "Halal" if all(all_criteria) else "Not Halal"
            reason = (
                "Stock is Shariah compliance."
                if status == "Halal"
                else "One or more financial criteria are not met."
            )

            return {
                "status": status,
                "reason": reason,
                "details": results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_ai_analysis(self) -> str | None:
        try:
            client = Groq(api_key=GROQ_API_KEY)

            results, market_cap = await self._validation_methods()

            prompt = f"""Provide a comprehensive analysis of {self.ticker} from multiple perspectives:
                1. Shariah Compliance Assessment
                2. Financial Health Overview
                3. Potential Ethical Concerns
                4. Recommendations for Islamic Investors
                Context:
                - Market Cap: ${market_cap}
                - Debt-Market Cap Ratio: {results['debt_cap_ratio'][1]}%
                - Non-Halal Income Ratio: {results['income_non_sharia_compliant_ratio'][1]}%
                - Cash-Market Cap ratio: {results['cash_cap_ratio'][1]}%
                - Liquidity Ratio: {results['liquidity_ratio'][1]}%
                Analyze considering AAOIFI and other Islamic financial standards.
            """

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}], model="llama3-70b-8192"
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def comprehensive_stock_screening(self) -> dict:
        financials = await self.financials.get_financials()

        return {
            "ticker": self.ticker.upper(),
            "long_name": financials["info"].get("longName", ""),
            "shariah_compliance": {
                "overall_compliant": await self.check_halal(),
            },
            "ai_analysis": await self.generate_ai_analysis(),
        }
