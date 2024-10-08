import repositories.main_repository as main_repo
from models.player import Player
from typing import List

TABLE_NAME = "players"


def find_all():
    query = f"select * from {TABLE_NAME}"
    res = main_repo.get_all(query)
    return [Player(**row) for row in res]


def find_one_by_id(player_id):
    query = f"select * from {TABLE_NAME} where id = {player_id}"
    res = main_repo.get_one(query)
    return Player(**res) if res else None


def insert(player: Player):
    query = f"INSERT INTO {TABLE_NAME}(name, player_str_id) VALUES (%s, %s)"
    return main_repo.make_insert_query(query, (player.name, player.player_str_id))


def find_player_by_str_id(str_id: str):
    query = f"select * from players where player_str_id = '{str_id}'"
    res = main_repo.get_one(query)
    return Player(**res) if res else None


def search_players_by_position_and_season(position: str, season: int = None):
    query = f"""
    select p."name" as player_name, p.player_str_id as player_id, t."name" as team, pos."type" as position, s."year" as season, psd.points, 
    psd.games, psd.threepercent as three_percents, psd.twopercent as two_percents, psd.assists, psd.turnovers    
    from players p 
    inner join player_position pp on p.id = pp.player_id 
    inner join positions pos on pos.id  = pp.position_id 
    inner join player_team pt on pt.player_id = p.id 
    inner join teams t on t.id = pt.team_id 
    inner join player_team_season pts on pts.player_team_id = pt.id 
    inner join seasons s on s.id = pts.season_id 
    inner join player_season_details psd on psd.player_team_season_id = pts.id 
    where pos."type" = '{position}'
    """
    if season:
        query += f' and s."year" = {season}'

    return main_repo.get_all(query)


def get_player_team_details(team_id: int):
    query = f'''
        select p."name" as player_name, t."name" as team, pos."type" as position, sum(psd.points) as points, 
        sum(psd.games) as games, avg(psd.twopercent) as two_percents, avg(psd.threepercent) as three_percents, 
        sum(psd.assists) as assists, sum(psd.turnovers) as turnovers  
        from players p 
        inner join player_team pt on pt.player_id  = p.id 
        inner join teams t on t.id = {team_id}
        inner join player_position pp on pp.player_id = p.id 
        inner join positions pos on pos.id = pp.position_id 
        inner join player_team_season pts on pt.id = pts.player_team_id 
        inner join player_season_details psd on pts.id = psd.player_team_season_id 
        where  p.id in (
        select pt2.player_id
        from teams t2
        inner join player_team pt2 on pt2.team_id = t2.id
        where t2.id = {team_id}
        )
        group by p.id, t."id" , pos.id
        '''
    return main_repo.get_all(query)


def get_players_by_ids(player_ids: List[int]):
    player_ids = ','.join(map(str, player_ids))
    query = f'''
    select pos."type" as position
    from players p 
    inner join player_position pp on pp.player_id = p.id 
    inner join positions pos on pos.id = pp.position_id 
    where p.id in ({player_ids})
    '''
    return main_repo.get_all(query)


def get_players_in_other_team(player_ids: List[int], team_id: int):
    player_ids = ','.join(map(str, player_ids))
    query = f'''
    select count(*)
    from players p 
    inner join player_position pp on pp.player_id = p.id 
    inner join positions pos on pos.id = pp.position_id 
    inner join player_team pt on pt.player_id = p.id 
    inner join teams t on t.id = pt.id 
    where t.is_real = false and t.id != {team_id}
    and p.id in ({player_ids})
    '''
    return main_repo.get_one(query)
