from datetime import datetime, timedelta, date, time
from typing import Union
from zoneinfo import ZoneInfo

from ics import Calendar, Event

from anime.season import get_season_now, deal_with_anime_data
from database.anime import query_year_anime, insert_season_anime


def get_future_weekdays(
        n: int,
        target_weekday: int,
        start_date: Union[datetime, str] = None,
        date_format: str = '%Y-%m-%dT%H:%M:%S%z',
):
    """
    获取未来 n 个指定星期几的日期

    参数:
    n -- 要获取的日期数量
    target_weekday -- 目标星期几 (0=周一, 1=周二, ..., 6=周日)
    start_date -- 起始日期 (默认为今天)，可以是 datetime 对象或字符串
    date_format -- 当 start_date 是字符串时的日期格式

    返回:
    包含未来 n 个目标星期几日期的列表
    """

    if start_date is None:
        start_date = datetime.today()
    elif isinstance(start_date, str):
        start_date = datetime.strptime(start_date, date_format)

    # 确保 start_date 是 datetime 对象
    if not isinstance(start_date, datetime):
        raise ValueError("start_date 必须是 datetime 对象或格式化的字符串")

    # 计算到下一个目标星期几的天数
    current_weekday = start_date.weekday()

    # 计算到下一个目标星期几的天数
    days_until_target = (target_weekday - current_weekday) % 7
    # 如果起始日期就是目标星期几且天数差为0，则从下一个周期开始
    if days_until_target == 0:
        days_until_target = 7

    # 计算第一个目标日期
    first_target_date = start_date + timedelta(days=days_until_target)

    # 生成所有目标日期
    result_dates = [
        first_target_date + timedelta(days=7 * i)
        for i in range(n)
    ]

    return result_dates


def convert_to_timezone_time(datetime_str: str, timezone: str = 'Asia/Tokyo') -> datetime:
    """
    将日期时间字符串转换为带 timezone 时区的 datetime 对象

    参数:
    datetime_str -- 日期时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
    timezone     -- 时区字符串，默认值为 Asia/Tokyo

    返回:
    带 timezone 时区的 datetime 对象
    """
    # 1. 解析输入字符串为无时区的 datetime 对象
    naive_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    # 2. 获取 Tokyo 时区
    timezone_tz = ZoneInfo(timezone)

    # 3. 将无时区 datetime 转换为 Tokyo 时区
    # 假设输入时间是 Tokyo 本地时间
    dt = naive_dt.replace(tzinfo=timezone_tz)

    return dt


def generate_anime_calendar_for_one_year() -> Calendar:
    today = datetime.today()
    dest_timezone = 'Asia/Shanghai'
    weekday_map = {
        'Sundays': 0,
        'Mondays': 1,
        'Tuesdays': 2,
        'Wednesdays': 3,
        'Thursdays': 4,
        'Fridays': 5,
        'Saturdays': 6,
    }

    anime_now_season_list = get_season_now()
    dataset = deal_with_anime_data(anime_now_season_list)
    insert_season_anime(dataset)
    anime_year_list = query_year_anime(today.year)

    # 创建一个日历对象
    calendar = Calendar()

    for anime in anime_year_list:
        title = anime['title']
        from_date = anime['from_date']
        duration = anime['duration']
        duration_unit = anime['duration_unit']
        day = anime['day']
        time = anime['time']
        from_timezone = anime['timezone']
        episodes = anime['episodes']

        tokyo_time = f'{from_date.split('T')[0]} {time}:00'
        chinese_time = convert_to_timezone_time(tokyo_time).astimezone(ZoneInfo(dest_timezone))

        target_weekday = weekday_map.get(day)
        future_weekdays = get_future_weekdays(episodes, target_weekday, chinese_time)

        for (i, weekday) in enumerate(future_weekdays):
            start_time = weekday
            end_time = weekday + timedelta(minutes=duration) if duration_unit == 'min' else weekday + timedelta(seconds=duration)

            event = Event()
            event.name = title
            event.begin = start_time.strftime("%Y-%m-%d %H:%M:%S")
            event.end = end_time.strftime("%Y-%m-%d %H:%M:%S")

            calendar.events.add(event)

    return calendar
