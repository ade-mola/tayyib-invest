from fastapi import HTTPException
from groq import Groq

from ..company_info.company import get_financials
from ..config import GROQ_API_KEY, LLM_PROMPT
from .business_activity import BusinessActivityValidator
from .financial_ratios import FinancialRatioScreener


class ValidateHalalStock:
    def __init__(self, ticker: str) -> None:
        """Initialize with the stock ticker."""

        self.ticker = ticker

    async def _validation_methods(self) -> tuple[dict, float, str]:
        """Run validation methods and return results."""

        financials = await get_financials(self.ticker)
        financial_ratios = FinancialRatioScreener(financials)
        business_activity = BusinessActivityValidator(financials["info"])
        latest_report = financials["financials"].name.strftime("%B %d, %Y")

        validation_methods = {
            "is_valid_business_activity": business_activity.is_valid_business_activity,
            "income_non_sharia_compliant_ratio": financial_ratios.income_non_sharia_compliant_ratio,
            "debt_cap_ratio": financial_ratios.debt_cap_ratio,
            "cash_cap_ratio": financial_ratios.cash_cap_ratio,
            "liquidity_ratio": financial_ratios.liquidity_ratio,
        }

        results = {name: method() for name, method in validation_methods.items()}
        return results, financials["info"].get("marketCap", 0.0), latest_report

    async def check_halal(self) -> dict:
        """Check if the stock is Halal based on screening factors."""

        try:
            results, _, latest_report = await self._validation_methods()

            all_criteria = [
                results.get("is_valid_business_activity", False),
                results["debt_cap_ratio"][0],
                results["cash_cap_ratio"][0],
                results["liquidity_ratio"][0],
                results["income_non_sharia_compliant_ratio"][0],
            ]

            status = "Halal" if all(all_criteria) else "Not Halal"
            reason = (
                "Stock is Shariah-compliant."
                if status == "Halal"
                else "One or more financial criteria are not met."
            )

            return {
                "latest_report_date": latest_report,
                "status": status,
                "reason": reason,
                "details": results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def generate_ai_analysis(self) -> str | None:
        """Generate AI analysis based on financial data."""

        try:
            client = Groq(api_key=GROQ_API_KEY)

            results, market_cap, latest_report = await self._validation_methods()

            prompt = LLM_PROMPT.format(
                self.ticker,
                latest_report,
                market_cap,
                results["is_valid_business_activity"],
                results["debt_cap_ratio"][1],
                results["income_non_sharia_compliant_ratio"][1],
                results["cash_cap_ratio"][1],
                results["liquidity_ratio"][1],
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Shariah-compliance finance expert and advisor.",
                    },
                    {"role": "user", "content": prompt},
                ],
                model="llama3-70b-8192",
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def comprehensive_stock_screening(self) -> dict:
        """Return a comprehensive stock screening."""

        financials = await get_financials(self.ticker)

        return {
            "ticker": self.ticker.upper(),
            "long_name": financials["info"].get("longName", ""),
            "shariah_compliance": {
                "overall_compliant": await self.check_halal(),
            },
            "ai_analysis": await self.generate_ai_analysis(),
        }
