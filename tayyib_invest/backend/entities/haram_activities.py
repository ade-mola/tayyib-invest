from enum import Enum


class HaramActivities(Enum):
    """
    Enum representing various haram activities with their associated keywords.
    Each activity is associated with a list of keywords that describe it.
    """

    ADULT_ENTERTAINMENT = ["Adult Entertainment", "Pornography", "Sexually Explicit Content"]
    ALCOHOL = ["Alcohol", "Beer", "Brewers", "Distilleries", "Liquor", "Wine", "Wineries"]
    FINANCE = ["Mortgage Finance", "Interest", "Capital Markets", "Banks"]
    GAMBLING = ["Casinos", "Gambling", "Betting", "Poker"]
    PORK = ["Pork", "Pig", "Swine", "Bacon"]
    TOBACCO = ["Tobacco", "Cigar"]
    WEAPONS = ["Weapons", "Arms", "Ammunition", "Firearms"]

    def __init__(self, keywords: list[str]) -> None:
        """
        Initialize the enum with a list of keywords.
        """
        self.keywords = keywords

    @property
    def get_keywords(self) -> list[str]:
        """
        Returns the list of keywords associated with the haram activity.
        """
        return self.keywords
