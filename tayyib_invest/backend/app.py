import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from requests import Request

from .company_info.company import search_company
from .entities.request import SearchRequest, TickerRequest
from .screener.validate_halal import ValidateHalalStock


app = FastAPI(title="Tayyib Invest API", description="API for halal stock validation")

origins = ["http://localhost:8000", "https://tayyib-invest.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust as necessary
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def read_health() -> dict:
    """Check health"""
    return {"status": "OK"}


@app.post("/v1/search")
async def search(request: SearchRequest) -> dict:
    """Search for a company based on the query provided in the request."""
    results = await search_company(request.query)
    return {"results": results}


@app.post("/v1/validate_halal_stock")
async def validate_halal_stock(request: TickerRequest) -> dict:
    """Validate if the given stock ticker is halal."""
    validator = ValidateHalalStock(request.ticker)
    results = await validator.check_halal()
    return {"compliance": results}


@app.post("/v1/generate_ai_analysis")
async def generate_ai_analysis(request: TickerRequest) -> str | None:
    """Generate AI analysis for the given stock ticker."""
    validator = ValidateHalalStock(request.ticker)
    content = await validator.generate_ai_analysis()
    return content


@app.post("/v1/comprehensive_screening")
async def comprehensive_screening(request: TickerRequest) -> dict:
    """Generate comprehensive screening for the given stock ticker."""
    validator = ValidateHalalStock(request.ticker)
    content = await validator.comprehensive_stock_screening()
    return content


@app.exception_handler(HTTPException)
async def global_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """Handle global HTTP exceptions and return a JSON response."""
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


if __name__ == "__main__":
    uvicorn.run("tayyib_invest.backend.app:app", host="0.0.0.0", port=8000, reload=True)
