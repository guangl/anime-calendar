from datetime import datetime

from dateutil.relativedelta import relativedelta
from pony.orm import db_session, select

from database.models import Anime


@db_session
def insert_season_anime(anime_list: list):
    try:
        for anime in anime_list:
            Anime(**anime)
    except Exception as e:
        print(f'insert error, because {e}')


@db_session
def query_year_anime(year: int = 2025):
    today = datetime.now()
    next_year_first_day = str(today + relativedelta(years=1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0))

    try:
        return Anime.select_by_sql("select * from anime where from_date is not null and year = $year and day is not null and time is not null and ( to_date is not null or to_date < $next_year_first_day );")[:]
    except Exception as e:
        print(f'query anime table error, because {e}')
        raise
        # return None
