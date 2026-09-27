# Todo List

Веб-приложение для задач на Python и Flask. Поддерживает добавление, редактирование,
удаление, смену статуса, фильтрацию и статистику.

## Запуск в Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "your-long-random-secret"
python run.py
```

Откройте `http://127.0.0.1:5000`. По умолчанию SQLite-база создаётся в
`instance/todo.db`. Для другого расположения задайте `DATABASE_URL`, например
`sqlite:///C:/data/todo.db`.

## Тесты

```powershell
python -m pytest -q
```
