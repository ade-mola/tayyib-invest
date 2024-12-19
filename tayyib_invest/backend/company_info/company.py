import httpx
import yfinance as yf
from fastapi import HTTPException

from tayyib_invest.config import FMP_API_KEY


async def search_company(query: str) -> list[dict[str, str]]:
    """Search for companies based on the provided query."""
    url = f"https://financialmodelingprep.com/api/v3/search?query={query}&apikey={FMP_API_KEY}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        return (
            [
                {
                    "name": f"{company['name']} ({company['symbol']})",
                    "symbol": company["symbol"],
                }
                for company in data
            ]
            if data
            else []
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def get_financials(ticker: str) -> dict:
    """Retrieve financial data for the given ticker."""
    if not ticker:
        raise ValueError("Ticker must be set to retrieve financials")

    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet
    financials = stock.financials
    info = stock.info

    if financials.empty or balance_sheet.empty:
        raise ValueError("Financial data unavailable")

    # get latest yearly info
    return {
        "info": info,
        "balance_sheet": balance_sheet.iloc[:, 0].to_dict(),
        "financials": financials.iloc[:, 0].to_dict(),
    }
