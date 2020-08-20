from datapipelines import CompositeDataTransformer

from .staticdata import StaticDataTransformer
from .status import StatusTransformer
from .leagues import LeagueTransformer
from .thirdpartycode import ThirdPartyCodeTransformer
from .summoner import SummonerTransformer


riotapi_transformer = CompositeDataTransformer(
    [
        StaticDataTransformer(),
        StatusTransformer(),
        LeagueTransformer(),
        ThirdPartyCodeTransformer(),
        SummonerTransformer(),
    ]
)

__transformers__ = [riotapi_transformer]
