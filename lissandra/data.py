from enum import Enum
import arrow


class Region(Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"

    @property
    def platform(self) -> "Platform":
        return getattr(Platform, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]

    @staticmethod
    def from_platform(platform):
        try:
            return platform.region
        except AttributeError:
            return Platform(platform).region

    @property
    def timezone(self) -> str:
        tzs = {
            "NA": "GMT-8",
            "LAN": "GMT-7",
            "LAS": "GMT-5",
            "BR": "GMT-4",
            "EUW": "GMT-2",
            "TR": "GMT-0",
            "EUNE": "GMT+1",
            "RU": "GMT+3",
            "KR": "GMT+6",
            "JP": "GMT+7",
            "OCE": "GMT+8",
        }
        return tzs[self.value]


class Platform(Enum):
    brazil = "BR1"
    europe_north_east = "EUN1"
    europe_west = "EUW1"
    japan = "JP1"
    korea = "KR"
    latin_america_north = "LA1"
    latin_america_south = "LA2"
    north_america = "NA1"
    oceania = "OC1"
    turkey = "TR1"
    russia = "RU"

    @property
    def region(self) -> "Region":
        return getattr(Region, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]

    @staticmethod
    def from_region(region):
        try:
            return region.platform
        except AttributeError:
            return Region(region).platform


DEFAULT_LOCALE = {
    Region.brazil: "pt_BR",
    Platform.brazil: "pt_BR",
    Region.europe_north_east: "en_GB",
    Platform.europe_north_east: "en_GB",
    Region.europe_west: "en_GB",
    Platform.europe_west: "en_GB",
    Region.japan: "ja_JP",
    Platform.japan: "ja_JP",
    Region.korea: "ko_KR",
    Platform.korea: "ko_KR",
    Region.latin_america_north: "es_MX",
    Platform.latin_america_north: "es_MX",
    Region.latin_america_south: "es_AR",
    Platform.latin_america_south: "es_AR",
    Region.north_america: "en_US",
    Platform.north_america: "en_US",
    Region.oceania: "en_AU",
    Platform.oceania: "en_AU",
    Region.turkey: "tr_TR",
    Platform.turkey: "tr_TR",
    Region.russia: "ru_RU",
    Platform.russia: "ru_RU",
}


class Resource(Enum):
    mana = "Mana"
    courage = "Courage"
    energy = "Energy"
    fury = "Fury"
    rage = "Rage"
    flow = "Flow"
    ferocity = "Ferocity"
    heat = "Heat"
    shield = "Shield"
    blood_well = "Blood Well"
    crimson_rush = "Crimson Rush"
    none = "None"
    no_cost = "No Cost"


class Tier(Enum):
    challenger = "CHALLENGER"
    grandmaster = "GRANDMASTER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    iron = "IRON"
    unranked = "UNRANKED"

    def __str__(self):
        return self.name.title()

    @staticmethod
    def _order():
        return {
            Tier.challenger: 9,
            Tier.grandmaster: 8,
            Tier.master: 7,
            Tier.diamond: 6,
            Tier.platinum: 5,
            Tier.gold: 4,
            Tier.silver: 3,
            Tier.bronze: 2,
            Tier.iron: 1,
        }

    def __lt__(self, other):
        return self._order()[self] < other._order()[other]

    def __gt__(self, other):
        return self._order()[self] > other._order()[other]

    def __le__(self, other):
        return self._order()[self] <= other._order()[other]

    def __ge__(self, other):
        return self._order()[self] >= other._order()[other]


class Division(Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"

    def __str__(self):
        return self.value

    @staticmethod
    def _order():
        return {Division.one: 4, Division.two: 3, Division.three: 2, Division.four: 1}

    def __lt__(self, other):
        return self._order()[self] < other._order()[other]

    def __gt__(self, other):
        return self._order()[self] > other._order()[other]

    def __le__(self, other):
        return self._order()[self] <= other._order()[other]

    def __ge__(self, other):
        return self._order()[self] >= other._order()[other]


class Rank:
    def __init__(self, tier: Tier, division: Division):
        self.tuple = (tier, division)
        self.tier = tier
        self.division = division

    def __str__(self):
        return "<{} {}>".format(self.tuple[0], self.tuple[1])

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __ne__(self, other):
        return self.tuple != other.tuple

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __gt__(self, other):
        return self.tuple > other.tuple

    def __le__(self, other):
        return self.tuple <= other.tuple

    def __ge__(self, other):
        return self.tuple >= other.tuple


class GameType(Enum):
    custom = "CUSTOM_GAME"
    tutorial = "TUTORIAL_GAME"
    matched = "MATCHED_GAME"


# References for Queues:
# https://developer.riotgames.com/game-constants.html
# https://discussion.developer.riotgames.com/articles/3482/multiple-queueids-are-being-updated-with-patch-719.html
# https://github.com/stelar7/L4J8/blob/master/src/main/java/no/stelar7/api/l4j8/basic/constants/types/GameQueueType.java
class Queue(Enum):
    custom = "CUSTOM"  # 0
    ranked_tft = "RANKED_TFT"  # 1100
    normal_tft = "NORMAL_TFT"  # 1090

    def from_id(self, id: int):
        return {i: season for season, i in QUEUE_IDS.items()}[id]

    @property
    def id(self):
        return QUEUE_IDS[self]


QUEUE_IDS = {
    # TODO: Check custom TFT queue number
    Queue.custom: 0,
    Queue.ranked_tft: 1100,  #  Convergence, Ranked Teamfight Tactics games
    Queue.normal_tft: 1090,  #  Convergence, Normal Teamfight Tactics games
}
