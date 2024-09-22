import repositories.main_repository as main_repo
import repositories.position_repository as position_repo
import repositories.season_repository as season_repo
import repositories.player_repository as player_repo
import repositories.team_repository as team_repo
import repositories.player_team_repository as player_team_repo
import repositories.player_position_repository as player_position_repo
import repositories.player_team_season_repository as player_team_season_repo
import repositories.player_season_details_repository as player_season_details_repo
from api.NBA_api import get_players_per_season
from models.NBA_api_object import NBAApiObject
from models.player import Player
from models.player_team import PlayerTeam
from models.player_team_season import PlayerTeamSeason
from models.position import Position
from models.season import Season
from models.player_position import PlayerPosition
from models.player_season_details import PlayerSeasonDetails
from typing import List
from toolz import *

from models.team import Team


def create_players_table():
    query = '''
    CREATE TABLE IF NOT EXISTS players(
            id SERIAL PRIMARY KEY,
            name VARCHAR(25) NOT NULL,
            player_str_id VARCHAR(25) NOT NULL
    ) 
    '''
    main_repo.make_structure_query(query)


def create_player_position_table():
    query = '''
        CREATE TABLE IF NOT EXISTS player_position(
                id SERIAL PRIMARY KEY,
                player_id INT NOT NULL,
                position_id INT NOT NULL,
                CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES players(id),
                CONSTRAINT fk_position FOREIGN KEY (position_id) REFERENCES positions(id)
        ) 
        '''
    main_repo.make_structure_query(query)


def create_player_season_details_table():
    query = '''
    CREATE TABLE IF NOT EXISTS player_season_details(
                id SERIAL PRIMARY KEY,
                player_team_season_id INT NOT NULL, 
                fieldGoals INT NOT NULL, 
                fieldAttempts INT NOT NULL, 
                fieldPercent FLOAT NOT NULL, 
                threeFg INT NOT NULL, 
                threeAttempts INT NOT NULL, 
                threePercent FLOAT NOT NULL, 
                twoFg INT NOT NULL, 
                twoAttempts INT NOT NULL, 
                twoPercent FLOAT NOT NULL, 
                assists INT NOT NULL, 
                turnovers INT NOT NULL, 
                games INT NOT NULL, 
                points INT NOT NULL,
                CONSTRAINT fk_player_team_season FOREIGN KEY (player_team_season_id) REFERENCES player_team_season(id)
    )
    '''
    main_repo.make_structure_query(query)


def create_player_team_table():
    query = '''
            CREATE TABLE IF NOT EXISTS player_team(
                    id SERIAL PRIMARY KEY,
                    player_id INT NOT NULL,
                    team_id INT NOT NULL,
                    CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES players(id),
                    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES teams(id)
            ) 
            '''
    main_repo.make_structure_query(query)


def create_player_team_season_table():
    query = '''
               CREATE TABLE IF NOT EXISTS player_team_season(
                       id SERIAL PRIMARY KEY,
                       player_team_id INT NOT NULL,
                       season_id INT NOT NULL,
                       CONSTRAINT fk_player_team FOREIGN KEY (player_team_id) REFERENCES player_team(id),
                       CONSTRAINT fk_season FOREIGN KEY (season_id) REFERENCES seasons(id)

               ) 
               '''
    main_repo.make_structure_query(query)


def create_positions_table():
    query = '''
               CREATE TABLE IF NOT EXISTS positions(
                       id SERIAL PRIMARY KEY,
                       type VARCHAR(25) NOT NULL
               ) 
               '''
    main_repo.make_structure_query(query)


def create_seasons_table():
    query = '''
                CREATE TABLE IF NOT EXISTS seasons(
                        id SERIAL PRIMARY KEY,
                        year INT NOT NULL
                ) 
                '''
    main_repo.make_structure_query(query)


def create_team_table():
    query = '''
               CREATE TABLE IF NOT EXISTS teams(
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(25) NOT NULL,
                       is_real BOOLEAN  NOT NULL
               ) 
               '''
    main_repo.make_structure_query(query)


def is_table_empty(table_name):
    query = f"SELECT COUNT(*) AS count FROM {table_name}"
    return main_repo.get_one(query)["count"] == 0


def seed_position_table():
    if is_table_empty("positions"):
        seed_data = [
            Position("C"),
            Position("PF"),
            Position("SF"),
            Position("SG"),
            Position("PG")
        ]
        for u in seed_data:
            position_repo.insert(u)


def seed_season_table():
    if is_table_empty("seasons"):
        seed_data = [
            Season(2022),
            Season(2023),
            Season(2024),
        ]
        for s in seed_data:
            season_repo.insert(s)


def fetch_NBA_api_data(year: int):
    res: List[NBAApiObject] = get_players_per_season(year)
    season = season_repo.find_one_by_year(year)
    positions: List[Position] = position_repo.find_all()
    for item in res:
        player = player_repo.find_player_by_str_id(item.playerId)
        if player is None:
            player = Player(name=item.playerName, player_str_id=item.playerId)
            player.id = player_repo.insert(player)

        team = team_repo.find_team_by_name(item.team)
        if team is None:
            team = Team(name=item.team, is_real=True)
            team.id = team_repo.insert(team)

        plyer_positions: List[PlayerPosition] = pipe(
            positions,
            partial(filter, lambda p: p.type in item.position.split("-")),
            partial(map, lambda p: PlayerPosition(player=player, position=p)),
            list,
        )
        for pp in plyer_positions:
            res = player_position_repo.find_one_by_player_id_and_position_id(pp.player.id, pp.position.id)
            if res is None:
                player_position_repo.insert(pp)

        player_team = player_team_repo.find_by_player_id_and_team_id(player.id, team.id)
        if player_team is None:
            player_team.id = player_team_repo.insert(player.id, team.id)

        player_team_season = PlayerTeamSeason(player_team=player_team, season=season)
        player_team_season.id = player_team_season_repo.insert(player_team_season)
        player_season_details = PlayerSeasonDetails(
            player_team_season=player_team_season,
            fieldGoals=item.fieldGoals,
            fieldAttempts=item.fieldAttempts,
            fieldPercent=item.fieldPercent if item.fieldPercent else 0,
            threeFg=item.threeFg,
            threeAttempts=item.threeAttempts,
            threePercent=item.threePercent if item.threePercent else 0,
            twoFg=item.twoFg,
            twoAttempts=item.twoAttempts,
            twoPercent=item.twoPercent if item.twoPercent else 0,
            assists=item.assists,
            turnovers=item.turnovers,
            games=item.games,
            points=item.points
        )
        player_season_details_repo.insert(player_season_details)


def run_seed():
    create_positions_table()
    create_seasons_table()
    create_team_table()
    create_players_table()
    create_player_position_table()
    create_player_team_table()
    create_player_team_season_table()
    create_player_season_details_table()

    seed_position_table()
    seed_season_table()
    if is_table_empty("players"):
        for year in [2022, 2023, 2024]:
            fetch_NBA_api_data(year)
