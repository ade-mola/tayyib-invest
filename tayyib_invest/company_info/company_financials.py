import yfinance as yf


class CompanyFinancials:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    async def get_financials(self) -> dict:
        if not self.ticker:
            raise ValueError("Ticker must be set to retrieve financials")

        stock = yf.Ticker(self.ticker)
        balance_sheet = stock.balance_sheet
        financials = stock.financials
        info = stock.info

        if financials.empty or balance_sheet.empty:
            raise ValueError("Financial data unavailable")

        # get latest yearly info
        balance_sheet = balance_sheet.iloc[:, 0].to_dict()
        financials = financials.iloc[:, 0].to_dict()

        return {"info": info, "balance_sheet": balance_sheet, "financials": financials}
