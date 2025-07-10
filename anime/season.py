from utils.request_with_retry import request_with_retry


def get_season_now() -> list:
    anime_list = []

    url = f'https://api.bgm.tv/calendar'
    response = request_with_retry(url)
    data = response

    # anime_list += data

    print(data)

    return anime_list
