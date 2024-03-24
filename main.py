"""
Запуск сервера - uvicorn main:app --host localhost --port 8000 --reload
З'эднання з базою даних - docker run --name contacts_app-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

Пошук по імені -  http://127.0.0.1:8000/api/contacts/?first_name=
Пошук по прізвищу -  http://127.0.0.1:8000/api/contacts/?last_name=
Пошук по email -  http://127.0.0.1:8000/api/contacts/?email=

Список контактів з днями народження на найближчі 7 днів - http://127.0.0.1:8000/api/contacts/?birthdays=7
Можна знайти список контактів на будь-яку кількість днів - змінити 7 на потрібну кількість днів
"""

from fastapi import FastAPI

from src.routes import contacts


app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "FastAPI Contacts"}


@app.get("/api/healthchecker")
def root():
    return {"message": "Is working."}
