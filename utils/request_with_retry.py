import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def request_with_retry(
        url: str,
        total=5,
        status_forcelist=None,
        allowed_methods=None,
        backoff_factor=1
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
        response = session.get(url)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Request ERROR: {e}')

        return None
