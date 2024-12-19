from pydantic import BaseModel


class TickerRequest(BaseModel):
    """Model for requesting a ticker symbol."""

    ticker: str


class SearchRequest(BaseModel):
    """Model for searching with a query string."""

    query: str
