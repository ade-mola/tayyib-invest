from unittest.mock import AsyncMock, patch

import pytest

from tayyib_invest.backend.screener.validate_halal import ValidateHalalStock


@pytest.mark.asyncio
async def test_validation_methods(validator: ValidateHalalStock, financials: dict) -> None:
    with patch(
        "tayyib_invest.backend.screener.validate_halal.get_financials", new_callable=AsyncMock
    ) as mock_get_financials:
        mock_get_financials.return_value = financials

        results, market_cap, latest_report = await validator._validation_methods()

        assert isinstance(results, dict)
        assert "is_valid_business_activity" in results
        assert "income_non_sharia_compliant_ratio" in results
        assert "debt_cap_ratio" in results
        assert "cash_cap_ratio" in results
        assert "liquidity_ratio" in results
        assert market_cap == 1000000
        assert latest_report == "January 01, 2024"


@pytest.mark.asyncio
async def test_check_halal_compliant(validator: ValidateHalalStock) -> None:
    with patch.object(validator, "_validation_methods", new_callable=AsyncMock) as mock_methods:
        mock_methods.return_value = (
            {
                "is_valid_business_activity": True,
                "income_non_sharia_compliant_ratio": (True, 3.0),
                "debt_cap_ratio": (True, 25.0),
                "cash_cap_ratio": (True, 25.0),
                "liquidity_ratio": (True, 35.0),
            },
            1000000,
            "January 01, 2024",
        )

        result = await validator.check_halal()

        assert result["status"] == "Halal"
        assert result["reason"] == "Stock is Shariah-compliant."
        assert "latest_report_date" in result
        assert "details" in result


@pytest.mark.asyncio
async def test_check_halal_non_compliant(validator: ValidateHalalStock) -> None:
    with patch.object(validator, "_validation_methods", new_callable=AsyncMock) as mock_methods:
        mock_methods.return_value = (
            {
                "is_valid_business_activity": False,
                "income_non_sharia_compliant_ratio": (True, 3.0),
                "debt_cap_ratio": (True, 25.0),
                "cash_cap_ratio": (True, 25.0),
                "liquidity_ratio": (True, 35.0),
            },
            1000000,
            "January 01, 2024",
        )

        result = await validator.check_halal()

        assert result["status"] == "Not Halal"
        assert result["reason"] == "One or more financial criteria are not met."


@pytest.mark.asyncio
async def test_comprehensive_stock_screening(
    validator: ValidateHalalStock,
    financials: dict,
) -> None:
    with (
        patch(
            "tayyib_invest.backend.screener.validate_halal.get_financials",
            new_callable=AsyncMock,
        ) as mock_get_financials,
        patch.object(validator, "check_halal", new_callable=AsyncMock) as mock_check_halal,
        patch.object(validator, "generate_ai_analysis", new_callable=AsyncMock) as mock_generate_ai,
    ):
        mock_get_financials.return_value = financials
        mock_check_halal.return_value = {"status": "Halal", "reason": "Stock is Shariah-compliant."}
        mock_generate_ai.return_value = "AI Analysis"

        result = await validator.comprehensive_stock_screening()

        assert result["ticker"] == "TEST"
        assert result["long_name"] == "Test Company Inc."
        assert result["shariah_compliance"]["overall_compliant"]["status"] == "Halal"
        assert result["ai_analysis"] == "AI Analysis"
