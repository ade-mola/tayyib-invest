from pydantic import BaseModel


class TickerRequest(BaseModel):
    ticker: str


class SearchRequest(BaseModel):
    query: str
