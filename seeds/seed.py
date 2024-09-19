import repositories.main_repository as main_repo
import repositories.position_repository as position_repo
import repositories.season_repository as season_repo
from models.position import Position
from models.season import Season


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
                    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES team(id)
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
               CREATE TABLE IF NOT EXISTS team(
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
