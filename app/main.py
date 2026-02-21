from fastapi import FastAPI, HTTPException

from app.config import load_config
from app.logger import logger
from app.models import User


config = load_config()

app = FastAPI(
    title="ServerKP1 - Practice 2",
    description="Работа с эндпоинтами, параметрами пути, запроса и тела",
    version="1.0.0",
)

# Фейковая база данных
fake_db = [
    {"username": "artur", "user_info": "любит колбасу"},
    {"username": "kolya", "user_info": "любит петь"},
    {"username": "katya", "user_info": "играет в футбол"},
    {"username": "olga", "user_info": "изучает python"},
]


@app.get("/")
async def root():
    logger.info("Запрос к корневому эндпоинту")
    return {"message": "Welcome to Practice 2 API", "docs": "/docs"}


# Параметры ЗАПРОСА
@app.get("/users/")
async def get_users(limit: int = 10, skip: int = 0):
    logger.info(f"Запрос списка пользователей: limit={limit}, skip={skip}")
    return fake_db[skip : skip + limit]


# Параметры ПУТИ
@app.get("/users/{username}")
async def get_user_by_name(username: str):
    logger.info(f"Поиск пользователя: {username}")
    for user in fake_db:
        if user["username"] == username:
            return user

    logger.warning(f"Пользователь {username} не найден")
    raise HTTPException(status_code=404, detail="User not found")


# Параметры ТЕЛА
@app.post("/add_user", response_model=User)
async def create_user(user: User):
    logger.info(f"Добавление нового пользователя: {user.username}")
    new_user = {"username": user.username, "user_info": user.user_info}
    fake_db.append(new_user)
    return user


# Удалени
@app.delete("/users/{username}")
async def delete_user(username: str):
    logger.info(f"Запрос на удаление пользователя: {username}")
    global fake_db
    user_to_delete = next((u for u in fake_db if u["username"] == username), None)

    if user_to_delete:
        fake_db = [u for u in fake_db if u["username"] != username]
        return {"message": f"User {username} deleted successfully"}

    logger.warning(f"Попытка удаления несуществующего пользователя: {username}")
    raise HTTPException(status_code=404, detail="User not found")
