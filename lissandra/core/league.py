from typing import List, Union, Optional, Generator, Set, Type

from merakicommons.cache import lazy_property, lazy
from merakicommons.container import searchable, SearchableList

from .. import configuration
from ..data import Region, Platform, Tier, Division, Queue
from .common import (
    CoreData,
    CoreDataList,
    CassiopeiaObject,
    CassiopeiaGhost,
    CassiopeiaLazyList,
    provide_default_region,
    ghost_load_on,
)
from ..dto.league import (
    LeagueDto,
    LeagueEntryDto,
    LeagueEntriesDto,
    LeagueSummonerEntriesDto,
    GrandmasterLeagueListDto,
    ChallengerLeagueListDto,
    MasterLeagueListDto,
)
from .summoner import Summoner


##############
# Data Types #
##############


class LeagueData(CoreData):
    """Contains the data for one League which has many entries."""

    _dto_type = LeagueDto
    _renamed = {"leagueId": "id"}

    def __call__(self, **kwargs):
        if "entries" in kwargs:
            self.entries = [LeagueEntryData(**entry) for entry in kwargs.pop("entries")]
        super().__call__(**kwargs)
        return self


class LeagueEntryData(CoreData):
    """Contains the data for one entry (summoner) in a League."""

    _dto_type = LeagueEntryDto
    _renamed = {"rank": "division"}

    def __call__(self, **kwargs):
        if "summonerId" in kwargs:
            self.summonerId = kwargs.pop("summonerId")
        super().__call__(**kwargs)
        return self


class LeagueSummonerEntriesData(CoreDataList):
    """League entries for a single summoner."""

    _dto_type = LeagueSummonerEntriesDto
    _renamed = {"summonerId": "summoner_id"}


class LeagueEntriesData(CoreDataList):
    """For paginated League entries."""

    _dto_type = LeagueEntriesDto
    _renamed = {}


class ChallengerLeagueListData(CoreData):
    _dto_type = ChallengerLeagueListDto
    _renamed = {"leagueId": "id"}

    def __call__(self, **kwargs):
        if "entries" in kwargs:
            self.entries = [LeagueEntryData(**entry) for entry in kwargs.pop("entries")]
        super().__call__(**kwargs)
        return self


class GrandmasterLeagueListData(CoreData):
    _dto_type = GrandmasterLeagueListDto
    _renamed = {"leagueId": "id"}

    def __call__(self, **kwargs):
        if "entries" in kwargs:
            self.entries = [LeagueEntryData(**entry) for entry in kwargs.pop("entries")]
        super().__call__(**kwargs)
        return self


class MasterLeagueListData(CoreData):
    _dto_type = MasterLeagueListDto
    _renamed = {"leagueId": "id"}

    def __call__(self, **kwargs):
        if "entries" in kwargs:
            self.entries = [LeagueEntryData(**entry) for entry in kwargs.pop("entries")]
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


@searchable(
    {
        str: ["division", "name", "summoner"],
        bool: ["hot_streak", "veteran", "fresh_blood"],
        Division: ["division"],
        Summoner: ["summoner"],
    }
)
class LeagueEntry(CassiopeiaGhost):
    _data_types = {LeagueEntryData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __eq__(self, other: "LeagueEntry"):
        if not isinstance(other, LeagueEntry) or self.region != other.region:
            return False
        return self.summoner == other.summoner and self._data[LeagueEntryData].name == other._data[LeagueEntryData].name

    __hash__ = CassiopeiaGhost.__hash__

    @classmethod
    def from_data(
        cls, data: LeagueEntryData, loaded_groups: Optional[Set[Type[CoreData]]] = None, league: "League" = None
    ):
        self = super().from_data(data=data, loaded_groups=loaded_groups)
        self.__league = league
        return self

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[LeagueEntryData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @lazy_property
    def tier(self) -> Tier:
        return Tier(self._data[LeagueEntryData].tier)

    @lazy_property
    def division(self) -> Division:
        return Division(self._data[LeagueEntryData].division)

    @lazy_property
    def queue(self) -> Queue:
        try:
            return Queue(self._data[LeagueEntryData].queue)
        except AttributeError:
            return self.league.queue

    @property
    def league_points(self) -> int:
        return self._data[LeagueEntryData].leaguePoints

    @property
    def wins(self) -> int:
        return self._data[LeagueEntryData].wins

    @property
    def losses(self) -> int:
        return self._data[LeagueEntryData].losses

    @property
    def fresh_blood(self) -> bool:
        return self._data[LeagueEntryData].freshBlood

    @property
    def hot_streak(self) -> bool:
        return self._data[LeagueEntryData].hotStreak

    @property
    def veteran(self) -> bool:
        return self._data[LeagueEntryData].veteran

    @property
    def inactive(self) -> bool:
        return self._data[LeagueEntryData].inactive

    @lazy_property
    def summoner(self) -> Summoner:
        return Summoner(
            id=self._data[LeagueEntryData].summonerId, name=self._data[LeagueEntryData].summonerName, region=self.region
        )

    @lazy_property
    def league(self) -> "League":
        return self.__league or League(id=self._data[LeagueEntryData].leagueId, region=self.region)


class LeagueEntries(CassiopeiaLazyList):  # type List[LeagueEntry]
    _data_types = {LeagueEntriesData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None, tier: Tier = None, division: Division = None):
        kwargs = {"region": region, "tier": tier, "division": division}
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(
        cls, *, region: Union[Region, str] = None, tier: Tier = None, division: Division = None
    ):
        query = {"region": region, "tier": tier, "division": division}
        return query

    @classmethod
    def from_generator(
        cls,
        generator: Generator,
        region: Union[Region, str] = None,
        tier: Tier = None,
        division: Division = None,
        **kwargs,
    ):
        self = cls.__new__(cls)
        kwargs["region"] = region
        kwargs["tier"] = tier
        kwargs["division"] = division
        CassiopeiaLazyList.__init__(self, generator=generator, **kwargs)
        return self

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LeagueEntriesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @lazy_property
    def tier(self) -> Tier:
        return Tier(self._data[LeagueEntriesData].tier)

    @lazy_property
    def division(self) -> Division:
        return Division(self._data[LeagueEntriesData].division)

    @lazy_property
    def queue(self) -> Queue:
        return Queue(self._data[LeagueEntriesData].queue)


class LeagueSummonerEntries(CassiopeiaLazyList):
    _data_types = {LeagueSummonerEntriesData}

    def __init__(self, *, summoner: Summoner):
        self.__summoner = summoner
        kwargs = {"region": summoner.region}
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, str]) -> dict:
        query = {"region": summoner.region}
        if isinstance(summoner, Summoner):
            query["summoner.id"] = summoner.id
        elif isinstance(summoner, str):
            if len(summoner) < 35:
                query["summoner.id"] = Summoner(name=summoner, region=summoner.region).id
            else:
                query["summoner.id"] = summoner
        assert "summoner.id" in query
        return query

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LeagueSummonerEntriesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    # This feels a little funky. The by-summoner/{encryptedSummonerId} endpoint returns a list
    # which only ever has one element, since there's only one ranked queue in TFT. It looks like
    # it was just copy+pasted from the League endpoint. Keeping this style for now, since it is
    # technically a list that's returned and there might be more elements in future.
    @lazy_property
    def tft(self):
        for entry in self:
            if entry.queue is Queue.ranked_tft:
                return entry
        raise ValueError("Queue does not exist for this summoner.")


@searchable({str: ["tier", "name"], Tier: ["tier"]})
class League(CassiopeiaGhost):
    _data_types = {LeagueData}

    def __init__(self, id: str = None, region: Union[Region, str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
            region = Region(region)
        kwargs = {"id": id, "region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"id": self.id, "region": self.region, "platform": self.platform}

    def __eq__(self, other: "League"):
        if not isinstance(other, League) or self.region != other.region:
            return False
        return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = self.id
        return "League(id={id_}, region='{region}')".format(id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LeagueData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def id(self) -> str:
        return self._data[LeagueData].id

    @CassiopeiaGhost.property(LeagueData)
    @ghost_load_on
    @lazy
    def tier(self) -> Tier:
        return Tier(self._data[LeagueData].tier)

    @CassiopeiaGhost.property(LeagueData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[LeagueData].name

    @CassiopeiaGhost.property(LeagueData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue(self._data[LeagueData].queue)

    @CassiopeiaGhost.property(LeagueData)
    @ghost_load_on
    @lazy
    def entries(self) -> List[LeagueEntry]:
        entries = []
        for entry in self._data[LeagueData].entries:
            entry.leagueId = self.id
            entry = LeagueEntry.from_data(data=entry, loaded_groups={LeagueEntriesData})
            entries.append(entry)
        return SearchableList(entries)


class ChallengerLeague(CassiopeiaGhost):
    _data_types = {ChallengerLeagueListData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __eq__(self, other: "ChallengerLeague"):
        if not isinstance(other, ChallengerLeague) or self.region != other.region:
            return False
        return True

    __hash__ = CassiopeiaGhost.__hash__

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ChallengerLeagueListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[ChallengerLeagueListData].id

    @lazy_property
    def tier(self) -> Tier:
        return Tier.challenger

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue(self._data[ChallengerLeagueListData].queue)

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[ChallengerLeagueListData].name

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on
    @lazy
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[ChallengerLeagueListData].entries])


class GrandmasterLeague(CassiopeiaGhost):
    _data_types = {GrandmasterLeagueListData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __eq__(self, other: "GrandmasterLeague"):
        if not isinstance(other, GrandmasterLeague) or self.region != other.region:
            return False
        return True

    __hash__ = CassiopeiaGhost.__hash__

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[GrandmasterLeagueListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(GrandmasterLeagueListData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[GrandmasterLeagueListData].id

    @lazy_property
    def tier(self) -> Tier:
        return Tier.grandmaster

    @CassiopeiaGhost.property(GrandmasterLeagueListData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue(self._data[GrandmasterLeagueListData].queue)

    @CassiopeiaGhost.property(GrandmasterLeagueListData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[GrandmasterLeagueListData].name

    @CassiopeiaGhost.property(GrandmasterLeagueListData)
    @ghost_load_on
    @lazy
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[GrandmasterLeagueListData].entries])


class MasterLeague(CassiopeiaGhost):
    _data_types = {MasterLeagueListData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __eq__(self, other: "MasterLeague"):
        if not isinstance(other, MasterLeague) or self.region != other.region:
            return False
        return True

    __hash__ = CassiopeiaGhost.__hash__

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MasterLeagueListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[MasterLeagueListData].id

    @lazy_property
    def tier(self) -> Tier:
        return Tier.master

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue(self._data[MasterLeagueListData].queue)

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[MasterLeagueListData].name

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on
    @lazy
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[MasterLeagueListData].entries])
