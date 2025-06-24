from datetime import datetime

from ics import Calendar

from anime.season import get_season_now, deal_with_anime_data
from database.anime import query_year_anime, insert_season_anime


def generate_anime_calendar_for_one_year() -> Calendar:
    today = datetime.today()

    # anime_now_season_list = get_season_now()
    # dataset = deal_with_anime_data(anime_now_season_list)
    # insert_season_anime(dataset)

    anime_year_list = query_year_anime(today.year)
    print(anime_year_list)

    # 创建一个日历对象
    calendar = Calendar()

    # # 创建一个事件
    # event = Event()
    # event.name = "会议：项目讨论"
    # event.begin = "2025-06-26 10:00:00"
    # event.end = "2025-06-26 11:00:00"
    # event.location = "会议室B"
    # event.description = "项目阶段性讨论会议"
    #
    # # 添加事件到日历
    # calendar.events.add(event)

    return calendar
