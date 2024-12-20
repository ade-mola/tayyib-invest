from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pandas as pd
import pytest
from fastapi import HTTPException

from tayyib_invest.backend.company_info.company import get_financials, search_company


@pytest.mark.asyncio
async def test_search_company_success() -> None:
    """Test successful company search with valid data."""

    mock_response = Mock()
    mock_response.json.return_value = [
        {"name": "Apple Inc.", "symbol": "AAPL"},
    ]
    mock_response.status_code = 200

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await search_company("apple")

        assert len(result) == 1
        assert result[0]["name"] == "Apple Inc. (AAPL)"
        assert result[0]["symbol"] == "AAPL"


@pytest.mark.asyncio
async def test_search_company_empty_response() -> None:
    """Test search with no matching results."""

    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.status_code = 200

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        result = await search_company("nonexistentcompany")

        assert result == []


@pytest.mark.asyncio
async def test_search_company_exception() -> None:
    """Test handling of exceptions."""

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = Exception(
            "Unexpected error"
        )

        with pytest.raises(HTTPException) as exc_info:
            await search_company("error")

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Unexpected error"


@pytest.mark.asyncio
async def test_get_financials(financials: dict) -> None:
    """Test getting financials."""

    with patch("tayyib_invest.backend.company_info.company.yf.Ticker") as mock_ticker:
        mock_instance = MagicMock()

        mock_instance.financials = pd.DataFrame(financials["financials"])
        mock_instance.balance_sheet = pd.DataFrame(financials["balance_sheet"])
        mock_instance.info = financials["info"]

        mock_ticker.return_value = mock_instance

        result = await get_financials("TEST")

        assert result["info"] == financials["info"]
        assert np.all(result["balance_sheet"] == financials["balance_sheet"])
        assert np.all(result["financials"] == financials["financials"])
