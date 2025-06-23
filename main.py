from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from ics import Calendar, Event
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_season_now(filter: str = 'tv', continuing: bool = True) -> list:
    anime_list = []

    # 创建一个 Retry 对象，设置重试策略
    retry_strategy = Retry(
        total=5,  # 最多重试 5 次
        status_forcelist=[429, 500, 502, 503, 504],  # 针对这些状态码重试
        allowed_methods=["GET"],  # 哪些请求方法允许重试（urllib3 >= 1.26.0 用 allowed_methods）
        backoff_factor=1  # 重试之间的等待时间: {backoff factor} * (2 ** (重试次数 - 1))
    )

    # 创建适配器
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # 创建 session
    session = requests.Session()
    session.mount('https://', adapter)

    # 发送请求
    try:
        page = 1
        has_next_page = True

        while has_next_page:
            url = f'https://api.jikan.moe/v4/seasons/now?filter={filter}&continuing={str(continuing).lower()}&page={page}'
            response = session.get(url)
            pagination = response.json().get('pagination')
            data = response.json().get('data')

            anime_list += data
            has_next_page = pagination.get('has_next_page')
            page += 1
    except requests.exceptions.RequestException as e:
        print(f'Request ERROR: {e}')

    return anime_list


def generate_calendar(anime_list: list) -> Calendar:
    # 创建一个日历对象
    calendar = Calendar()

    for anime in anime_list:
        event = Event()

        try:
            title = anime.get('title')
            from_date = (
                datetime.strptime(to_str, '%Y-%m-%dT%H:%M:%S%z')
                if (to_str := anime.get('aired', {}).get('from')) else None
            )
            to_date = (
                datetime.strptime(to_str, '%Y-%m-%dT%H:%M:%S%z')
                if (to_str := anime.get('aired', {}).get('to')) else None
            )
            duration = int(anime.get('duration').split(' ')[0])
            duration_unit = anime.get('duration').split(' ')[1]
            day = anime.get('broadcast').get('day')
            time = anime.get('broadcast').get('time')
            timezone = anime.get('broadcast').get('timezone')

            if day is None or time is None:
                raise Exception('day is none or time is none')

            base_time = datetime.strptime(time, '%H:%M').time()
            start_time = datetime.combine(from_date, base_time, tzinfo=ZoneInfo(timezone)).astimezone(ZoneInfo("Asia/Shanghai"))
            end_time = start_time + (
                timedelta(minutes=duration) if duration_unit == 'min' else timedelta(seconds=duration)
            )

            print(f'{start_time} - {end_time}')

        except Exception as e:
            print(f'has error: {e}, the anime is {anime}')
            continue
            # raise

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


if __name__ == '__main__':
    # # 保存为 .ics 文件
    # with open('my_calendar.ics', 'w', encoding='utf-8') as f:
    #     f.writelines(calendar)

    anime_list = get_season_now()
    calendar = generate_calendar(anime_list)
