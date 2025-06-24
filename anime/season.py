from utils.request_with_retry import request_with_retry


def get_season_now(filter: str = 'tv', continuing: bool = True) -> list:
    anime_list = []

    page = 1
    has_next_page = True

    while has_next_page:
        url = f'https://api.jikan.moe/v4/seasons/now?filter={filter}&continuing={str(continuing).lower()}&page={page}'
        response = request_with_retry(url)
        pagination = response.get('pagination')
        data = response.get('data')

        anime_list += data
        has_next_page = pagination.get('has_next_page')
        page += 1

    return anime_list


def deal_with_anime_data(anime_list: list) -> list:
    dataset = []

    for anime in anime_list:
        try:
            mal_id = anime.get('mal_id')
            title = anime.get('title')
            from_date = anime.get('aired', {}).get('from')
            to_date = anime.get('aired', {}).get('to')
            season = anime.get('season')
            year = anime.get('year')
            duration = (
                int(anime.get('duration').split()[0])
                if anime.get('duration') != 'Unknown'
                else None
            )
            duration_unit = (
                anime.get('duration').split()[1]
                if anime.get('duration') != 'Unknown'
                else None
            )
            day = anime.get('broadcast').get('day')
            time = anime.get('broadcast').get('time')
            timezone = anime.get('broadcast', {}).get('timezone')
            episodes = anime.get('episodes')

            if all(item.get('mal_id') != mal_id for item in dataset):
                anime = {
                    'mal_id': mal_id,
                    'title': title,
                    'from_date': from_date,
                    'to_date': to_date,
                    'season': season,
                    'year': year,
                    'duration': duration,
                    'duration_unit': duration_unit,
                    'day': day,
                    'time': time,
                    'timezone': timezone,
                    'episodes': episodes
                }

                dataset.append(anime)
        except Exception as e:
            print(f'has error: {e}, the anime is {anime}')
            raise
            # continue

    return dataset
