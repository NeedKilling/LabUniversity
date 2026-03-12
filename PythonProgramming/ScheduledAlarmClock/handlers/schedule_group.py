import json
from .file_handler import groupJson
from datetime import datetime


def buttons(callback_data,GROUP,metod):

    schedule = groupJson(GROUP, metod)
    match callback_data:
        case "today":            
            today = datetime.now().strftime("%d.%m.%Y")
            for day in schedule:
                if day["date"] == today:
                    result = format_day_schedule(day)
                    return result
            return "На сегодня занятий нет"

        case "tomorrow":
            pass
        case "week":
            pass

def format_day_schedule(day_data):
    """Форматирует данные одного дня для вывода"""
    if not day_data or "lessons" not in day_data or len(day_data["lessons"]) == 0:
        return f"{day_data.get('date', 'Неизвестная дата')} - Занятий нет"
    
    result = []
    result.append(f"📅 <b>{day_data['date']}</b> - {day_data['day']}")
    result.append("━" * 30)
    
    for i, lesson in enumerate(day_data["lessons"], 1):
        lesson_text = (
            f"{i}. <b>{lesson['time']}</b>\n"
            f"   📚 {lesson['Discipline']}\n"
            f"   🏢 {lesson.get('Building', 'Корпус не указан')}, ауд. {lesson.get('numberAud', 'не указана')}\n"
            f"   👨‍🏫 {lesson.get('Teacher', 'Преподаватель не указан')}"
        )
        result.append(lesson_text)
    
    return "\n".join(result)
# def is_valid_group_name(text):

#     pattern1 = r'^[А-ЯЁ]{2,10}-\d{1,3}[а-яё]{0,5}$'
    
#     return (bool(re.match(pattern1, text)))



# def send_schedule(GROUP,group_json, metod):
#     schedule = groupJson()



# def get_today_schedule(group_name):
#     """Возвращает расписание на сегодня"""
#     schedule = load_schedule(group_name)
#     if not schedule:
#         return None
    
#     today = datetime.now().strftime("%d.%m.%Y")
    
#     for day in schedule:
#         if day.get("date") == today:
#             return day
    
#     return None

# def get_week_schedule(group_name):
#     """Возвращает расписание на всю неделю"""
#     schedule = load_schedule(group_name)
#     if not schedule:
#         return None
    
#     # Получаем текущую дату и дату через 7 дней
#     today = datetime.now()
#     week_later = today.replace(day=today.day + 7)
    
#     week_schedule = []
#     for day in schedule:
#         try:
#             day_date = datetime.strptime(day["date"], "%d.%m.%Y")
#             if today <= day_date <= week_later:
#                 week_schedule.append(day)
#         except:
#             continue
    
#     return week_schedule

# def get_day_schedule(group_name, date_str):
#     """Возвращает расписание на конкретную дату"""
#     schedule = load_schedule(group_name)
#     if not schedule:
#         return None
    
#     for day in schedule:
#         if day.get("date") == date_str:
#             return day
    
#     return None