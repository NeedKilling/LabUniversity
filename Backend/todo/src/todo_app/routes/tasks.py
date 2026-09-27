from collections import defaultdict
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from ..extensions import db
from ..forms import TaskForm
from ..models import Task


tasks_bp = Blueprint("tasks", __name__)


def get_task_or_404(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, description=f"Задача №{task_id} не найдена.")
    return task


def get_statistics():
    total = db.session.scalar(db.select(func.count()).select_from(Task)) or 0
    completed = db.session.scalar(db.select(func.count()).select_from(Task).where(Task.is_completed.is_(True))) or 0
    return total, completed


def get_dashboard_metrics():
    """Calculate actionable, non-completed task counts for the dashboard."""
    today = date.today()
    upcoming_end = today + timedelta(days=7)
    active = Task.is_completed.is_(False)
    count = lambda *conditions: db.session.scalar(
        db.select(func.count()).select_from(Task).where(active, *conditions)
    ) or 0
    return {
        "due_today": count(Task.due_date == today),
        "overdue": count(Task.due_date < today),
        "next_seven_days": count(Task.due_date > today, Task.due_date <= upcoming_end),
        "later": count(Task.due_date > upcoming_end),
        "high_priority": count(Task.priority == 1),
        "medium_priority": count(Task.priority == 2),
        "low_priority": count(Task.priority == 3),
    }


def date_group_label(due_date):
    """Return a short Russian date label without relying on system locale."""
    if due_date is None:
        return "Без даты"
    if due_date == date.today():
        return "Сегодня"
    if due_date == date.today() + timedelta(days=1):
        return "Завтра"
    months = (
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    )
    return f"{due_date.day} {months[due_date.month - 1]}"


def group_tasks_by_due_date(tasks):
    """Order date groups as today, upcoming, overdue, then undated."""
    grouped = defaultdict(list)
    for task in tasks:
        grouped[task.due_date].append(task)

    today = date.today()
    future_dates = sorted(due for due in grouped if due is not None and due > today)
    past_dates = sorted((due for due in grouped if due is not None and due < today), reverse=True)
    ordered_dates = ([today] if today in grouped else []) + future_dates + past_dates
    if None in grouped:
        ordered_dates.append(None)
    return [{"label": date_group_label(due), "tasks": grouped[due]} for due in ordered_dates]


@tasks_bp.get("/")
def home():
    today = date.today()
    tasks = db.session.execute(
        db.select(Task).where(Task.due_date == today).order_by(Task.created_at.desc(), Task.id.desc())
    ).scalars().all()
    total, completed = get_statistics()
    return render_template("tasks/home.html", tasks=tasks, total=total, completed=completed, today=today)


@tasks_bp.get("/tasks")
def index():
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    query = db.select(Task)

    if status == "open":
        query = query.where(Task.is_completed.is_(False))
    elif status == "completed":
        query = query.where(Task.is_completed.is_(True))
    if priority in {"1", "2", "3"}:
        query = query.where(Task.priority == int(priority))

    tasks = db.session.execute(query.order_by(Task.created_at.desc(), Task.id.desc())).scalars().all()
    total, completed = get_statistics()
    return render_template(
        "tasks/index.html",
        groups=group_tasks_by_due_date(tasks),
        total=total,
        completed=completed,
        status=status,
        priority=priority,
    )


@tasks_bp.get("/dashboard")
def dashboard():
    total, completed = get_statistics()
    return render_template(
        "tasks/dashboard.html", total=total, completed=completed, metrics=get_dashboard_metrics()
    )


@tasks_bp.route("/tasks/new", methods=["GET", "POST"])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=(form.description.data or "").strip() or None,
            priority=int(form.priority.data),
            due_date=form.due_date.data,
        )
        db.session.add(task)
        db.session.commit()
        flash(f"Задача №{task.id} добавлена.", "success")
        return redirect(url_for("tasks.home"))
    return render_template("tasks/form.html", form=form, heading="Новая задача", task=None)


@tasks_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = (form.description.data or "").strip() or None
        task.priority = int(form.priority.data)
        task.due_date = form.due_date.data
        db.session.commit()
        flash(f"Задача №{task.id} обновлена.", "success")
        return redirect(url_for("tasks.home"))
    return render_template("tasks/form.html", form=form, heading=f"Редактирование задачи №{task.id}", task=task)


@tasks_bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = get_task_or_404(task_id)
    task.is_completed = not task.is_completed
    db.session.commit()
    flash(f"Задача №{task.id}: статус изменён.", "success")
    if request.form.get("next") == "home":
        return redirect(url_for("tasks.home"))
    return redirect(url_for("tasks.index", **request.args))


@tasks_bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = get_task_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Задача №{task_id} удалена.", "success")
    return redirect(url_for("tasks.home"))
