import os
from pathlib import Path

from flask import Flask, render_template
from sqlalchemy import inspect, text

from .extensions import csrf, db


def create_app(test_config=None):
    """Create and configure the Todo List application."""
    app = Flask(__name__, instance_relative_config=True)
    default_database = f"sqlite:///{Path(app.instance_path) / 'todo.db'}"

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", default_database),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)

    from .routes.tasks import date_group_label, tasks_bp

    app.register_blueprint(tasks_bp)
    app.jinja_env.filters["date_group_label"] = date_group_label

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html", error=error), 404

    with app.app_context():
        db.create_all()
        # Lightweight migration for databases created before task dates existed.
        columns = {column["name"] for column in inspect(db.engine).get_columns("tasks")}
        if "due_date" not in columns:
            with db.engine.begin() as connection:
                connection.execute(text("ALTER TABLE tasks ADD COLUMN due_date DATE"))
        if "description" not in columns:
            with db.engine.begin() as connection:
                connection.execute(text("ALTER TABLE tasks ADD COLUMN description VARCHAR(1000)"))

    return app
