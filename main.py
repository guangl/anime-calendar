import tomllib
from datetime import datetime, timedelta

import requests
from ics import Calendar, Event
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def request_with_retry(
        url: str,
        total=5,
        status_forcelist=None,
        allowed_methods=None,
        backoff_factor=1,
        headers=None
):
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]
    if allowed_methods is None:
        allowed_methods = ['GET']

    try:
        # 创建一个 Retry 对象，设置重试策略
        retry_strategy = Retry(
            total=total,  # 最多重试 5 次
            status_forcelist=status_forcelist,  # 针对这些状态码重试
            allowed_methods=allowed_methods,  # 哪些请求方法允许重试（urllib3 >= 1.26.0 用 allowed_methods）
            backoff_factor=backoff_factor  # 重试之间的等待时间: {backoff factor} * (2 ** (重试次数 - 1))
        )

        # 创建适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)

        # 创建 session
        session = requests.Session()
        session.mount('https://', adapter)
        response = session.get(url, headers=headers)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Request ERROR: {e}')

        return None


def calculate_end_time(start_str: str, duration_str: str):
    # 解析开始时间
    start = datetime.strptime(start_str, '%Y-%m-%d %H:%M')

    # 解析持续时间
    h, m, s = map(int, duration_str.split(':'))
    delta = timedelta(hours=h, minutes=m, seconds=s)

    # 计算结束时间
    end = start + delta
    return end.strftime('%Y-%m-%d %H:%M')


def get_anime_detail(anime_id: int):
    url = f'https://api.bgm.tv/v0/episodes?subject_id={anime_id}'
    headers = {
        'User-Agent': 'guangl/anime-calendar (https://github.com/guangl/anime-calendar)'
    }

    response = request_with_retry(url, headers=headers)

    return response.get('data')


def get_anime_broadcast(anime_name: str):
    page = 1
    pagination = {'has_next_page': True}

    while pagination.get('has_next_page'):
        url = f'https://api.jikan.moe/v4/seasons/now?filter=tv&page={page}&limit=25'
        response = request_with_retry(url)
        pagination = response.get('pagination')

        for anime in response.get('data'):
            if anime.get('title_japanese') == anime_name:
                return anime.get('broadcast').get('time')

        page += 1

    return None


def get_season_now() -> list:
    anime_list = []
    want_anime_details = []

    with open("config.toml", "rb") as f:
        config_data = tomllib.load(f)

    url = f'https://api.bgm.tv/calendar'
    response = request_with_retry(url)

    for animates in response:
        anime_list += animates.get('items')

    for anime in anime_list:
        if anime.get('name_cn') in config_data.get('want').get('animates'):
            anime_detail = get_anime_detail(anime.get('id'))

            want_anime_details.append({
                'name': anime.get('name'),
                'name_cn': anime.get('name_cn'),
                'episodes': anime_detail,
                'time': get_anime_broadcast(anime.get('name'))
            })

    anime_episodes = []
    for episode in want_anime_details:
        for every_episode in episode.get('episodes'):
            if every_episode.get('name') != '' or every_episode.get('name_cn') != '':
                episode_name = every_episode.get('name_cn') if every_episode.get('name_cn') else every_episode.get(
                    'name')

                anime_episodes.append({
                    'anime_name_cn': episode.get('name_cn'),
                    'airdate': every_episode.get('airdate'),
                    'episode_name': episode_name,
                    'ep': every_episode.get('ep'),
                    'duration': every_episode.get('duration') if every_episode.get('duration') else '00:24:00',
                    'time': episode.get('time')
                })

    return anime_episodes


def generate_anime_calendar() -> Calendar:
    anime_now_season_list = get_season_now()

    calendar = Calendar()
    for anime in anime_now_season_list:
        start_time = f'{anime.get('airdate')} {anime.get('time')}'

        event = Event()
        event.name = f'{anime.get('anime_name_cn')} - 第 {anime.get('ep')} 集：{anime.get('episode_name')}'
        event.begin = f'{start_time}:00'
        event.end = calculate_end_time(start_time, anime.get('duration'))

        calendar.events.add(event)

    return calendar


def generate_calendar() -> None:
    anime_calendar = generate_anime_calendar()

    merged_calendar = Calendar()
    for e in anime_calendar.events:
        merged_calendar.events.add(e)

    # 保存合并后的日历
    with open('calendar.ics', 'w', encoding='UTF-8') as f:
        f.writelines(merged_calendar.serialize_iter())


if __name__ == '__main__':
    generate_calendar()
