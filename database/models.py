from pathlib import Path

from pony.orm import PrimaryKey, Required, Optional, Database, db_session, set_sql_debug

db_path = (Path() / 'dist' / 'calendar.db').resolve()
db = Database()
db.bind(provider='sqlite', filename=str(db_path), create_db=True)


class Anime(db.Entity):
    _table_ = 'anime'

    id = PrimaryKey(int, auto=True)
    mal_id = Required(int, unique=True)
    title = Required(str)
    from_date = Optional(str, nullable=True)
    to_date = Optional(str, nullable=True)
    season = Optional(str, nullable=True)
    year = Optional(int)
    duration = Optional(int)
    duration_unit = Optional(str, nullable=True)
    day = Optional(str, nullable=True)
    time = Optional(str, nullable=True)
    timezone = Optional(str, nullable=True)
    episodes = Optional(int)


def init_database():
    set_sql_debug(True)
    db.generate_mapping(create_tables=True)
