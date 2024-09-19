from repositories.position_repository import find_one_by_position


def check_search_players_validation(position: str, season: str):
    res1 = position and find_one_by_position(position)
    res2 = True if season is None else is_str_can_convert_to_int(season)
    return res1 and res2


def is_str_can_convert_to_int(num_as_str):
    try:
        year = int(num_as_str)
        return True
    except Exception as e:
        return False


