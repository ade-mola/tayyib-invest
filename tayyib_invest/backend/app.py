# from collections.abc import Any, Callable, Coroutine

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from requests import Request

from tayyib_invest.backend.company_info.search_company import search_company
from tayyib_invest.backend.entities.request import SearchRequest, TickerRequest
from tayyib_invest.backend.screener.validate_halal import ValidateHalalStock


app = FastAPI(title="Tayyib Invest API", description="API for halal stock validation")

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust as necessary
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.post("/v1/search")
async def search(request: SearchRequest) -> dict:
    results = await search_company(request.query)
    return {"results": results}


@app.post("/v1/validate_halal_stock")
async def validate_halal_stock(request: TickerRequest) -> dict:
    validator = ValidateHalalStock(request.ticker)
    results = await validator.check_halal()
    return {"compliance": results}


@app.post("/v1/generate_ai_analysis")
async def generate_ai_analysis(request: TickerRequest) -> str | None:
    validator = ValidateHalalStock(request.ticker)
    content = await validator.generate_ai_analysis()
    return content


@app.post("/v1/comprehensive_screening")
async def comprehensive_screening(request: TickerRequest) -> dict:
    validator = ValidateHalalStock(request.ticker)
    content = await validator.comprehensive_stock_screening()
    return content


@app.exception_handler(HTTPException)
async def global_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)