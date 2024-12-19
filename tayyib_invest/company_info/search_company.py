import httpx
from fastapi import HTTPException

from tayyib_invest.config import FMP_API_KEY


async def search_company(query: str) -> list[dict[str, str]]:
    url = f"https://financialmodelingprep.com/api/v3/search?query={query}&apikey={FMP_API_KEY}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        if not data:
            return []

        results = [
            {
                "name": f"{company['name']} ({company['symbol']})",
                "symbol": company["symbol"],
            }
            for company in data
        ]
        return results

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
