from itertools import chain

from tayyib_invest.backend.entities.haram_activities import HaramActivities


class BusinessActivityValidator:
    def __init__(self, info: dict) -> None:
        self.industry = info.get("industry", "").lower()
        self.sector = info.get("sector", "").lower()
        # self.summary = info.get("longBusinessSummary", "").lower()
        self.description_sources = [self.industry, self.sector]

    @property
    def haram_activities(self) -> list:
        """Return a list of haram activities."""
        return [activity.lower() for activity in chain(*[activities.value for activities in HaramActivities])]

    def is_valid_business_activity(self) -> bool:
        """Check if the activity is halal."""
        desc = " ".join(filter(bool, self.description_sources)).lower()

        return not any(haram_activity in desc for haram_activity in self.haram_activities)
