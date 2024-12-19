from enum import Enum


# add comment on aerospace & defense companies
#
# haram_industries = [
#         'Conventional Banking',
#         'Conventional Financial Services',
#         'Conventional Insurance',
#         'Weapons and Defense',
#         'Adult Entertainment',
# ]


class HaramSectors(Enum):
    ADULT_ENTERTAINMENT = "Adult Entertainment"
    ALCOHOL = "Alcohol"
    BANKS = "Banks"
    BEVERAGES_B = "Beverages - Brewers"
    BEVERAGES_WD = "Beverages - Wineries & Distilleries"
    CAPITAL_MARKETS = "Capital Markets"
    CASINOS = "Casinos"
    GAMBLING = "Gambling"
    INTEREST = "Interest"
    MORTGAGE = "Mortgage Finance"
    PORK = "Pork"
    PORNOGRAPHY = "Pornography"
    TOBACCO = "Tobacco"


class BusinessSectorValidator:
    def __init__(self, info: dict) -> None:
        self.sector = info.get("industry", "").lower()

    @property
    def haram_sectors(self) -> list:
        """Return a list of haram sectors."""
        return [sector.value.lower() for sector in HaramSectors]

    def is_valid_sector(self) -> bool:
        """Check if the sector is halal."""
        return not any(haram_sector in self.sector for haram_sector in self.haram_sectors)
