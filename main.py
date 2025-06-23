from ics import Calendar, Event

# 创建一个日历对象
calendar = Calendar()

# 创建一个事件
event = Event()
event.name = "会议：项目讨论"
event.begin = "2025-06-25 10:00:00"
event.end = "2025-06-25 11:00:00"
event.location = "会议室A"
event.description = "项目阶段性讨论会议"

# 添加事件到日历
calendar.events.add(event)

# 可以继续添加更多事件...

if __name__ == '__main__':
    # 保存为 .ics 文件
    with open('my_calendar.ics', 'w', encoding='utf-8') as f:
        f.writelines(calendar)

