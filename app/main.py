from typing import Annotated, List

from fastapi import FastAPI, Form, Query, UploadFile

from app.config import load_config
from app.logger import logger
from app.models import Item, User, UserResponse


# Загружаем конфигурацию
config = load_config()

app = FastAPI(
    title="ServerKP1 - Practice 3",
    description="Формы, файлы, вложенные модели и продвинутые параметры",
    version="1.0.0",
)


@app.get("/")
async def root():
    logger.info("Запрос к корневому эндпоинту")
    return {"message": "Welcome to Practice 3 API", "docs": "/docs"}


#  ОБРАБОТКА ФОРМ (Form)
@app.post("/register/")
async def register_user(
    username: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    age: Annotated[int, Form(...)],
    password: Annotated[str, Form(...)],
):
    logger.info(f"Регистрация через форму: {username}")
    return {
        "username": username,
        "email": email,
        "age": age,
        "password_length": len(password),
    }


#  ВЛОЖЕННЫЕ МОДЕЛИ И JSON (response_model)
@app.post("/users/nested", response_model=UserResponse)
async def create_nested_user(user: User):
    logger.info(f"Создание юзера с вложенной моделью: {user.name}")
    # Возвращаем словарь, который FastAPI сам преобразует в модель UserResponse
    return {"message": f"Пользователь {user.name} создан!", "user": user}


#  ЗАГРУЗКА ФАЙЛОВ (UploadFile)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    logger.info(f"Загрузка файла: {file.filename}")
    content = await file.read()  # Читаем файл в память
    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "content_type": file.content_type,
    }


@app.post("/multiple-files/")
async def upload_multiple_files(files: List[UploadFile]):
    logger.info(f"Загрузка нескольких файлов. Количество: {len(files)}")
    return {"filenames": [file.filename for file in files]}


# ПРОДВИНУТЫЕ ПАРАМЕТРЫ ЗАПРОСА (Query) и ОБЪЕКТ ITEM
@app.post("/items/")
async def create_item(item: Item):
    logger.info(f"Создан Item: {item.name}")
    return item


@app.get("/items/")
async def read_items(
    skip: Annotated[int, Query(alias="start", ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    logger.info(f"Запрос списка Items. start={skip}, limit={limit}")
    return {"skip_or_start": skip, "limit": limit}


# СМЕШИВАНИЕ ПАРАМЕТРОВ ПУТИ И ЗАПРОСА
@app.get("/users/{user_id}")
async def read_user(user_id: int, is_admin: bool = False):
    logger.info(f"Запрос юзера {user_id}. Админ: {is_admin}")
    return {"user_id": user_id, "is_admin": is_admin}
