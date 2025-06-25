import sqlite3
from pathlib import Path

db_path = (Path() / 'dist' / 'calendar.db').resolve()


def init_database():
    create_anime_sql = '''
        CREATE TABLE IF NOT EXISTS "anime" (
          "id" INTEGER PRIMARY KEY AUTOINCREMENT,
          "mal_id" INTEGER UNIQUE NOT NULL,
          "title" TEXT NOT NULL,
          "from_date" TEXT,
          "to_date" TEXT,
          "season" TEXT,
          "year" INTEGER,
          "duration" INTEGER,
          "duration_unit" TEXT,
          "day" TEXT,
          "time" TEXT,
          "timezone" TEXT,
          "episodes" INTEGER
        );
    '''

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(create_anime_sql)


def insert_season_anime(anime_list: list):
    insert_anime_sql = '''
        INSERT OR IGNORE INTO anime(
            mal_id, title, from_date, to_date, season, year, duration, duration_unit,day, time, timezone, episodes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    with sqlite3.connect(db_path) as connection:
        # 性能优化设置
        connection.execute("PRAGMA journal_mode = WAL")  # 写前日志模式
        connection.execute("PRAGMA synchronous = NORMAL")  # 平衡安全性和性能
        connection.execute("PRAGMA cache_size = -10000")  # 10MB 缓存

        cursor = connection.cursor()

        connection.isolation_level = None
        cursor.execute("BEGIN")
        try:
            for anime in anime_list:
                cursor.execute(insert_anime_sql, anime)

            cursor.execute("COMMIT")
        except sqlite3.Error as sqlite_error:
            print(f'insert sqlite error: {sqlite_error}')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def query_year_anime(year: int = 2025):

    query_year_anime_sql = '''
        select * from anime where year = ? and from_date is not null and to_date is not null and day is not null and time is not null
    '''

    try:
        with sqlite3.connect(db_path) as connection:
            connection.row_factory = dict_factory  # 设置行工厂

            cursor = connection.cursor()
            cursor.execute(query_year_anime_sql, (year,))
            rows = cursor.fetchall()

            return rows
    except sqlite3.Error as sqlite_error:
        print(f'query sqlite error: {sqlite_error}')
        return None
