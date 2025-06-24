from pathlib import Path

from pony.orm import PrimaryKey, Required, Optional, Database

db_path = (Path() / 'dist' / 'calendar.db').resolve()
db = Database()
db.bind(provider='sqlite', filename=str(db_path), create_db=True)


class Anime(db.Entity):
    __table__ = 'anime'

    id = PrimaryKey(int, auto=True)
    mal_id = Required(int, unique=True)
    title = Required(str)
    from_date = Optional(str)
    to_date = Optional(str)
    season = Optional(str)
    year = Optional(int)
    duration = Optional(int)
    duration_unit = Optional(str)
    day = Optional(str)
    time = Optional(str)
    timezone = Optional(str)
    episodes = Optional(int)


def init_database():
    db.generate_mapping(create_tables=True)
