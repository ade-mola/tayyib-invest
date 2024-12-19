from ..entities.haram_activities import HaramActivities


class BusinessActivityValidator:
    def __init__(self, info: dict) -> None:
        """Initialize with company info."""
        self.industry = info.get("industry", "").lower()
        self.sector = info.get("sector", "").lower()
        # self.summary = info.get("longBusinessSummary", "").lower()
        self.description_sources = [self.industry, self.sector]

    @property
    def haram_activities(self) -> list:
        """Return a list of haram activities."""
        return [
            keyword.lower() for activity in HaramActivities for keyword in activity.get_keywords
        ]

    def is_valid_business_activity(self) -> bool:
        """Check if the activity is halal."""
        desc = " ".join(filter(bool, self.description_sources)).lower()

        return not any(haram_activity in desc for haram_activity in self.haram_activities)
