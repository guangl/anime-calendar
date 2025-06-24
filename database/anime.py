from pony.orm import db_session

from database.models import Anime


@db_session
def insert_season_anime(anime_list: list):
    try:
        Anime.bulk_insert(anime_list)
    except Exception as e:
        print(f'insert error, because {e}')


@db_session
def query_year_anime(year: int = 2025):
    try:
        return Anime.get(year=year)
    except Exception as e:
        print(f'query anime table error, because {e}')
        return None
