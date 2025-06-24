from anime.calendar import generate_anime_calendar_for_one_year
from database.models import init_database


def generate_calendar() -> None:
    anime_calendar = generate_anime_calendar_for_one_year()

    # merged_calendar = Calendar()
    # for e in anime_calendar.events:
    #     merged_calendar.events.add(e)
    #
    # # 保存合并后的日历
    # with open('calendar.ics', 'w') as f:
    #     f.writelines(merged_calendar.serialize_iter())


if __name__ == '__main__':
    init_database()
    generate_calendar()
