from datapipelines import CompositeDataTransformer

from .staticdata import StaticDataTransformer
from .status import StatusTransformer
from .leagues import LeagueTransformer
from .thirdpartycode import ThirdPartyCodeTransformer
from .tft_summoner import TFTSummonerTransformer


riotapi_transformer = CompositeDataTransformer(
    [
        StaticDataTransformer(),
        StatusTransformer(),
        LeagueTransformer(),
        ThirdPartyCodeTransformer(),
        TFTSummonerTransformer(),
    ]
)

__transformers__ = [riotapi_transformer]
