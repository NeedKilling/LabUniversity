from datetime import date, timedelta

from todo_app.extensions import db
from todo_app.models import Task


def create_task(client, title="Первая задача", priority="1", due_date=None, description=""):
    return client.post(
        "/tasks/new",
        data={
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date or date.today().isoformat(),
        },
        follow_redirects=True,
    )


def test_create_task_assigns_id_and_defaults_to_open(client, app):
    response = create_task(client)
    assert response.status_code == 200
    with app.app_context():
        task = db.session.scalar(db.select(Task))
        assert task.id == 1
        assert task.is_completed is False
        assert task.priority == 1


def test_rejects_blank_title_and_invalid_priority(client, app):
    response = create_task(client, "   ", "7")
    assert response.status_code == 200
    assert "Введите название задачи" in response.text or "Название не может" in response.text
    with app.app_context():
        assert db.session.scalar(db.select(Task)) is None


def test_toggle_updates_stats_and_filters(client, app):
    create_task(client, "Закрываемая задача", "3")
    create_task(client, "Открытая задача", "1")
    with app.app_context():
        first = db.session.scalar(db.select(Task).where(Task.title == "Закрываемая задача"))
        first_id = first.id
    response = client.post(f"/tasks/{first_id}/toggle", follow_redirects=True)
    assert "Выполнено" in response.text
    dashboard = client.get("/dashboard")
    assert "Осталось</p><strong>1" in dashboard.text
    filtered = client.get("/tasks?status=completed")
    assert "Закрываемая задача" in filtered.text
    assert "Открытая задача" not in filtered.text


def test_edit_delete_and_unknown_task(client, app):
    create_task(client)
    with app.app_context():
        task = db.session.scalar(db.select(Task))
        task_id = task.id
    client.post(f"/tasks/{task_id}/edit", data={"title": "Изменённая", "priority": "2", "due_date": date.today().isoformat()})
    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.title == "Изменённая"
        assert task.priority == 2
    deleted = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    assert "На сегодня задач нет" in deleted.text
    assert client.get("/tasks/999/edit").status_code == 404


def test_home_shows_only_tasks_due_today(client):
    create_task(client, "Сегодня", due_date=date.today().isoformat())
    create_task(client, "Завтра", due_date=(date.today() + timedelta(days=1)).isoformat())
    home = client.get("/")
    assert "Сегодня" in home.text
    assert "Завтра" not in home.text
    all_tasks = client.get("/tasks")
    assert "Сегодня" in all_tasks.text
    assert "Завтра" in all_tasks.text


def test_all_tasks_grouped_by_date_and_filter_is_automatic(client):
    today = date.today()
    create_task(client, "Сегодня", due_date=today.isoformat())
    create_task(client, "Завтра", due_date=(today + timedelta(days=1)).isoformat())
    create_task(client, "Через неделю", due_date=(today + timedelta(days=7)).isoformat())
    create_task(client, "Вчера", due_date=(today - timedelta(days=1)).isoformat())

    response = client.get("/tasks")
    assert "В работе" in response.text
    assert "Фильтр" not in response.text
    assert 'onchange="this.form.submit()"' in response.text
    assert response.text.index("Сегодня") < response.text.index("Завтра")
    assert response.text.index("Завтра") < response.text.index("Через неделю")
    assert response.text.index("Через неделю") < response.text.index("Вчера")


def test_priority_picker_is_rendered(client):
    response = client.get("/tasks/new")
    assert response.status_code == 200
    assert "priority-choice-1" in response.text
    assert "Срочные и важные дела" in response.text


def test_description_is_saved_and_shown_on_task_card(client, app):
    create_task(client, "Задача с описанием", description="Важные детали для выполнения")
    with app.app_context():
        task = db.session.scalar(db.select(Task))
        assert task.description == "Важные детали для выполнения"
    response = client.get("/")
    assert "Важные детали для выполнения" in response.text
    assert "Открыть →" not in response.text


def test_dashboard_deadline_and_priority_metrics(client):
    today = date.today()
    create_task(client, "Сегодня", "1", today.isoformat())
    create_task(client, "Просрочено", "2", (today - timedelta(days=1)).isoformat())
    create_task(client, "На неделе", "3", (today + timedelta(days=3)).isoformat())
    create_task(client, "Позже", "1", (today + timedelta(days=10)).isoformat())
    response = client.get("/dashboard")
    assert "Просрочено" in response.text
    assert "Приоритеты активных задач" in response.text
    assert "Задачи по срокам" in response.text
    assert "const complete=0,remaining=4,high=2,medium=1,low=1,overdue=1,today=1,week=1,later=1" in response.text
