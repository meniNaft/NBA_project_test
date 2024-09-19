from requests import get
from typing import List
from models.NBA_api_object import NBAApiObject
NBA_API_URL = "http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?pageSize=20&&season="


def get_players_per_season(year) -> List[NBAApiObject]:
    try:
        response = get(NBA_API_URL + f"{year}")
        res = response.json()
        return [NBAApiObject(**{k: v for k, v in row.items() if k in NBAApiObject.__annotations__}) for row in res]
    except Exception as e:
        print(e)
        return []
