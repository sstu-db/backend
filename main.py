from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import MetaData, create_engine, inspect, text

# Настройте параметры подключения к PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/app"

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
inspector = inspect(engine)

app = FastAPI()

# Разрешаем CORS (настройте список allowed origins по необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модель для запроса SQL
class QueryRequest(BaseModel):
    query: str


@app.get("/tables")
def get_tables():
    """
    Возвращает список таблиц в базе данных.
    """
    try:
        tables = inspector.get_table_names()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tables/{table_name}")
def get_table_info(table_name: str):
    """
    Возвращает информацию о колонках указанной таблицы.
    """
    try:
        # Получаем информацию о колонках
        columns = inspector.get_columns(table_name)

        # Преобразуем данные в сериализуемый формат
        columns_info = [
            {"name": column["name"], "type": str(column["type"])} for column in columns
        ]

        return {"table": table_name, "columns": columns_info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def execute_query(query_request: QueryRequest):
    """
    Выполняет SQL-запрос, переданный в теле запроса.
    """
    query_str = query_request.query
    try:
        with engine.connect() as connection:
            # Выполняем запрос с использованием text()
            result = connection.execute(text(query_str))

            # Получаем имена колонок из объекта ResultProxy
            columns = (
                result.keys() if result.returns_rows else []
            )  # Получаем имена колонок, если результат есть

            # Извлекаем все строки результата
            rows = (
                [dict(zip(columns, row)) for row in result.fetchall()]
                if result.returns_rows
                else []
            )

        return {"result": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
