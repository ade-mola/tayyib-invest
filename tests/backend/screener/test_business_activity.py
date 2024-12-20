from tayyib_invest.backend.screener.business_activity import BusinessActivityValidator


def test_is_valid_business_activity() -> None:
    """Test is_valid_business_activity method."""
    info = {"industry": "Technology", "sector": "Information Technology"}
    validator = BusinessActivityValidator(info)
    assert validator.is_valid_business_activity() is True

    info_haram = {"industry": "Adult Entertainment", "sector": "Entertainment"}
    validator_haram = BusinessActivityValidator(info_haram)
    assert validator_haram.is_valid_business_activity() is False
