from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import MetaData, create_engine, inspect, text
from typing import List, Optional
from datetime import date, datetime

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


# 1. Получить тренеров (дата рождения, имя, фамилия, отчество, специальности) клиента.
@app.get("/clients/{client_id}/trainers")
def get_client_trainers(client_id: int):
    """
    Получить тренеров (дата рождения, имя, фамилия, отчество, специальности) клиента.
    """
    try:
        query = """
        SELECT 
            p.id, p.дата_рождения, p.имя, p.фамилия, p.отчество,
            ARRAY_AGG(DISTINCT st.название) as специальности
        FROM 
            тренер_и_клиент tic
        JOIN 
            тренер t ON tic.тренер_id = t.id
        JOIN 
            пользователь p ON t.пользователь_id = p.id
        JOIN 
            тренер_и_специальность tis ON t.id = tis.тренер_id
        JOIN 
            специальность_тренера st ON tis.специальность_тренера_id = st.id
        WHERE 
            tic.клиент_id = :client_id
        GROUP BY 
            p.id, p.дата_рождения, p.имя, p.фамилия, p.отчество
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(query), {"client_id": client_id})
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"trainers": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. Получить клиентов (дата рождения, имя, фамилия, отчество, цель тренировок, уровень подготовки) тренера.
@app.get("/trainers/{trainer_id}/clients")
def get_trainer_clients(trainer_id: int):
    """
    Получить клиентов (дата рождения, имя, фамилия, отчество, цель тренировок, уровень подготовки) тренера.
    """
    try:
        query = """
        SELECT 
            p.id, p.дата_рождения, p.имя, p.фамилия, p.отчество,
            up.название as уровень_подготовки,
            ARRAY_AGG(DISTINCT zt.название) as цели_тренировок
        FROM 
            тренер_и_клиент tic
        JOIN 
            клиент k ON tic.клиент_id = k.id
        JOIN 
            пользователь p ON k.пользователь_id = p.id
        JOIN 
            уровень_подготовки up ON k.уровень_подготовки_id = up.id
        JOIN 
            клиент_и_цель_тренировок kzt ON k.id = kzt.клиент_id
        JOIN 
            цель_тренировок zt ON kzt.цель_тренировок_id = zt.id
        WHERE 
            tic.тренер_id = :trainer_id
        GROUP BY 
            p.id, p.дата_рождения, p.имя, p.фамилия, p.отчество, up.название
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(query), {"trainer_id": trainer_id})
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"clients": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 3. Получить план тренировок (название, описание, тренировки) клиента, либо тренера, либо по клиента и тренера.
@app.get("/training-plans")
def get_training_plans(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None
):
    """
    Получить план тренировок (название, описание, тренировки) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        query = """
        WITH упражнения AS (
            SELECT 
                u.id, u.название, u.описание,
                jsonb_build_object(
                    'id', тип_упр.id,
                    'название', тип_упр.название
                ) as тип_упражнения,
                jsonb_build_object(
                    'id', su.id,
                    'название', su.название
                ) as сложность_упражнения,
                (
                    SELECT ARRAY_AGG(
                        jsonb_build_object(
                            'id', m.id,
                            'название', m.название,
                            'приоритет', pm.название
                        )
                    )
                    FROM упражнение_и_мыщца um
                    JOIN мышца m ON um.мышца_id = m.id
                    JOIN приоритет_мышцы pm ON um.приоритет_мышцы_id = pm.id
                    WHERE um.упражнение_id = u.id
                ) as мышцы,
                (
                    SELECT ARRAY_AGG(s.название)
                    FROM упражнение_и_снаряжение us
                    JOIN снаряжение s ON us.снаряжение_id = s.id
                    WHERE us.упражнение_id = u.id
                ) as снаряжение
            FROM 
                упражнение u
            JOIN 
                тип_упражнения тип_упр ON u.тип_упражнения_id = тип_упр.id
            JOIN 
                сложность_упражнения su ON u.сложность_упражнения_id = su.id
            GROUP BY 
                u.id, u.название, u.описание, тип_упр.id, тип_упр.название, su.id, su.название
        ),
        тренировка_и_упражнения AS (
            SELECT 
                tuu.тренировка_id,
                ARRAY_AGG(
                    jsonb_build_object(
                        'id', tuu.id,
                        'номер_в_очереди', tuu.номер_в_очереди,
                        'колво_подходов', tuu.колво_подходов,
                        'колво_подходов_выполнено', tuu.колво_подходов_выполнено,
                        'колво_повторений', tuu.колво_повторений,
                        'колво_повторений_выполнено', tuu.колво_повторений_выполнено,
                        'упражнение', jsonb_build_object(
                            'id', у.id,
                            'название', у.название,
                            'описание', у.описание,
                            'тип_упражнения', у.тип_упражнения,
                            'сложность_упражнения', у.сложность_упражнения,
                            'мышцы', у.мышцы,
                            'снаряжение', у.снаряжение
                        )
                    ) ORDER BY tuu.номер_в_очереди
                ) AS тренировка_и_упражнение
            FROM 
                тренировка_и_упражнение tuu
            JOIN 
                упражнения у ON tuu.упражнение_id = у.id
            GROUP BY 
                tuu.тренировка_id
        ),
        тренировки_с_упражнениями AS (
            SELECT 
                t.id, t.название, t.является_онлайн, t.время_начала, t.чат_id,
                tt.название as вид_тренировки,
                т.тренировка_и_упражнение
            FROM 
                тренировка t
            JOIN 
                тренировка_и_упражнение tuu ON t.id = tuu.тренировка_id
            JOIN 
                упражнение u ON tuu.упражнение_id = u.id
            JOIN 
                тип_тренировки tt ON u.тип_упражнения_id = tt.id
            LEFT JOIN 
                тренировка_и_упражнения т ON t.id = т.тренировка_id
            GROUP BY 
                t.id, t.название, t.является_онлайн, t.время_начала, t.чат_id, tt.название, т.тренировка_и_упражнение
        )
        SELECT 
            pt.id, pt.название, pt.описание,
            ARRAY_AGG(
                DISTINCT jsonb_build_object(
                    'id', т.id,
                    'название', т.название,
                    'является_онлайн', т.является_онлайн,
                    'время_начала', т.время_начала,
                    'чат_id', т.чат_id,
                    'вид_тренировки', т.вид_тренировки,
                    'тренировка_и_упражнение', т.тренировка_и_упражнение
                )
            ) as тренировки
        FROM 
            план_тренировки pt
        JOIN 
            тренировка_и_план_тренировки tpt ON pt.id = tpt.план_тренировки_id
        JOIN 
            тренировки_с_упражнениями т ON tpt.тренировка_id = т.id
        JOIN 
            план_тренировки_и_пользователь ptp ON pt.id = ptp.план_тренировки_id
        JOIN 
            пользователь p ON ptp.пользователь_id = p.id
        WHERE 
            1=1
        """
        
        params = {}
        
        if client_id:
            query += " AND p.id = (SELECT пользователь_id FROM клиент WHERE id = :client_id)"
            params["client_id"] = client_id
            
        if trainer_id:
            query += " AND p.id = (SELECT пользователь_id FROM тренер WHERE id = :trainer_id)"
            params["trainer_id"] = trainer_id
            
        query += " GROUP BY pt.id, pt.название, pt.описание"
        
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"training_plans": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 4. Получить тренировки (название, формат проведения, время начала, вид тренировки, упражнения) клиента, либо тренера, либо по клиента и тренера.
@app.get("/workouts")
def get_workouts(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None
):
    """
    Получить тренировки (название, формат проведения, время начала, вид тренировки, упражнения) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        query = """
        WITH упражнения AS (
            SELECT 
                u.id, u.название, u.описание,
                jsonb_build_object(
                    'id', тип_упр.id,
                    'название', тип_упр.название
                ) as тип_упражнения,
                jsonb_build_object(
                    'id', su.id,
                    'название', su.название
                ) as сложность_упражнения,
                (
                    SELECT ARRAY_AGG(
                        jsonb_build_object(
                            'id', m.id,
                            'название', m.название,
                            'приоритет', pm.название
                        )
                    )
                    FROM упражнение_и_мыщца um
                    JOIN мышца m ON um.мышца_id = m.id
                    JOIN приоритет_мышцы pm ON um.приоритет_мышцы_id = pm.id
                    WHERE um.упражнение_id = u.id
                ) as мышцы,
                (
                    SELECT ARRAY_AGG(s.название)
                    FROM упражнение_и_снаряжение us
                    JOIN снаряжение s ON us.снаряжение_id = s.id
                    WHERE us.упражнение_id = u.id
                ) as снаряжение
            FROM 
                упражнение u
            JOIN 
                тип_упражнения тип_упр ON u.тип_упражнения_id = тип_упр.id
            JOIN 
                сложность_упражнения su ON u.сложность_упражнения_id = su.id
            GROUP BY 
                u.id, u.название, u.описание, тип_упр.id, тип_упр.название, su.id, su.название
        ),
        тренировка_и_упражнения AS (
            SELECT 
                tuu.тренировка_id,
                ARRAY_AGG(
                    jsonb_build_object(
                        'id', tuu.id,
                        'номер_в_очереди', tuu.номер_в_очереди,
                        'колво_подходов', tuu.колво_подходов,
                        'колво_подходов_выполнено', tuu.колво_подходов_выполнено,
                        'колво_повторений', tuu.колво_повторений,
                        'колво_повторений_выполнено', tuu.колво_повторений_выполнено,
                        'упражнение', jsonb_build_object(
                            'id', у.id,
                            'название', у.название,
                            'описание', у.описание,
                            'тип_упражнения', у.тип_упражнения,
                            'сложность_упражнения', у.сложность_упражнения,
                            'мышцы', у.мышцы,
                            'снаряжение', у.снаряжение
                        )
                    ) ORDER BY tuu.номер_в_очереди
                ) AS тренировка_и_упражнение
            FROM 
                тренировка_и_упражнение tuu
            JOIN 
                упражнения у ON tuu.упражнение_id = у.id
            GROUP BY 
                tuu.тренировка_id
        )
        SELECT 
            t.id, t.название, t.является_онлайн, t.время_начала,
            tt.название as вид_тренировки,
            т.тренировка_и_упражнение
        FROM 
            тренировка t
        JOIN 
            тренировка_и_пользователь тп ON t.id = тп.тренировка_id
        JOIN 
            пользователь p ON тп.пользователь_id = p.id
        JOIN 
            тренировка_и_упражнение tuu ON t.id = tuu.тренировка_id
        JOIN 
            упражнение u ON tuu.упражнение_id = u.id
        JOIN 
            тип_тренировки tt ON u.тип_упражнения_id = tt.id
        LEFT JOIN 
            тренировка_и_упражнения т ON t.id = т.тренировка_id
        WHERE 
            1=1
        """
        
        params = {}
        
        if client_id:
            query += " AND p.id = (SELECT пользователь_id FROM клиент WHERE id = :client_id)"
            params["client_id"] = client_id
            
        if trainer_id:
            query += " AND p.id = (SELECT пользователь_id FROM тренер WHERE id = :trainer_id)"
            params["trainer_id"] = trainer_id
            
        query += " GROUP BY t.id, t.название, t.является_онлайн, t.время_начала, tt.название, т.тренировка_и_упражнение"
        
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"workouts": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 5. Получить упражнения (название, тип, уровень сложности, описание, мышцы с указанием важности этой мышцы в упражнении, снаряжение) клиента, либо тренера, либо по клиента и тренера.
@app.get("/exercises")
def get_exercises(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None
):
    """
    Получить упражнения (название, тип, уровень сложности, описание, мышцы с указанием важности этой мышцы в упражнении, снаряжение) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        query = """
        SELECT 
            u.id, u.название, u.описание,
            jsonb_build_object(
                'id', tu.id,
                'название', tu.название
            ) as тип_упражнения,
            jsonb_build_object(
                'id', su.id,
                'название', su.название
            ) as сложность_упражнения,
            ARRAY_AGG(DISTINCT jsonb_build_object(
                'мышца_id', m.id,
                'название_мышцы', m.название,
                'приоритет', pm.название
            )) as мышцы,
            ARRAY_AGG(DISTINCT s.название) as снаряжение
        FROM 
            упражнение u
        JOIN 
            тип_упражнения tu ON u.тип_упражнения_id = tu.id
        JOIN 
            сложность_упражнения su ON u.сложность_упражнения_id = su.id
        JOIN 
            упражнение_и_мыщца um ON u.id = um.упражнение_id
        JOIN 
            мышца m ON um.мышца_id = m.id
        JOIN 
            приоритет_мышцы pm ON um.приоритет_мышцы_id = pm.id
        JOIN 
            упражнение_и_снаряжение us ON u.id = us.упражнение_id
        JOIN 
            снаряжение s ON us.снаряжение_id = s.id
        JOIN 
            упражнение_и_пользователь up ON u.id = up.упражнение_id
        JOIN 
            пользователь p ON up.пользователь_id = p.id
        WHERE 
            1=1
        """
        
        params = {}
        
        if client_id:
            query += " AND p.id = (SELECT пользователь_id FROM клиент WHERE id = :client_id)"
            params["client_id"] = client_id
            
        if trainer_id:
            query += " AND p.id = (SELECT пользователь_id FROM тренер WHERE id = :trainer_id)"
            params["trainer_id"] = trainer_id
            
        query += " GROUP BY u.id, u.название, u.описание, tu.id, tu.название, su.id, su.название"
        
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"exercises": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 6. Получить дневники состояния (дата записи, текстовая заметка, файл) по пользователю и диапазону дат.
@app.get("/diaries")
def get_diaries(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Получить дневники состояния (дата записи, текстовая заметка, файл) по пользователю и диапазону дат.
    """
    try:
        query = """
        SELECT 
            д.id, д.дата, д.запись,
            jsonb_build_object(
                'id', ф.id,
                'имя_файла', ф.имя_файла,
                'типы_файлов', (
                    SELECT ARRAY_AGG(тф.название)
                    FROM файл_и_тип_файла фтф
                    JOIN тип_файла тф ON фтф.тип_файла_id = тф.id
                    WHERE фтф.файл_id = ф.id
                )
            ) as файл,
            ARRAY_AGG(DISTINCT ч.название) as чувства,
            ARRAY_AGG(DISTINCT пч.название) as причины_чувств
        FROM 
            дневник д
        JOIN 
            дневник_и_чувство дч ON д.id = дч.дневник_id
        JOIN 
            чувство ч ON дч.чувство_id = ч.id
        JOIN 
            дневник_и_причина_чувства дпч ON д.id = дпч.дневник_id
        JOIN 
            причина_чувства пч ON дпч.причина_чувства_id = пч.id
        LEFT JOIN 
            файл ф ON д.файл_id = ф.id
        WHERE 
            д.пользователь_id = :user_id
        """
        
        params = {"user_id": user_id}
        
        if start_date:
            query += " AND д.дата >= :start_date"
            params["start_date"] = start_date
            
        if end_date:
            query += " AND д.дата <= :end_date"
            params["end_date"] = end_date
            
        query += " GROUP BY д.id, д.дата, д.запись, ф.id, ф.имя_файла"
        
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"diaries": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 7. Получить шаги (количество шагов, цель шагов, дата записи) по пользователю и диапазону дат.
@app.get("/steps")
def get_steps(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Получить шаги (количество шагов, цель шагов, дата записи) по пользователю и диапазону дат.
    """
    try:
        query = """
        SELECT 
            ш.id, ш.колво, ш.целевое_колво, ш.дата
        FROM 
            шаги ш
        WHERE 
            ш.пользователь_id = :user_id
        """
        
        params = {"user_id": user_id}
        
        if start_date:
            query += " AND ш.дата >= :start_date"
            params["start_date"] = start_date
            
        if end_date:
            query += " AND ш.дата <= :end_date"
            params["end_date"] = end_date
            
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"steps": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 8. Получить потребление воды (объем выпитой воды, цель, дата) по пользователю и диапазону дат.
@app.get("/water")
def get_water(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Получить потребление воды (объем выпитой воды, цель, дата) по пользователю и диапазону дат.
    """
    try:
        query = """
        SELECT 
            в.id, в.объем, в.целевой_объем, в.дата
        FROM 
            вода в
        WHERE 
            в.пользователь_id = :user_id
        """
        
        params = {"user_id": user_id}
        
        if start_date:
            query += " AND в.дата >= :start_date"
            params["start_date"] = start_date
            
        if end_date:
            query += " AND в.дата <= :end_date"
            params["end_date"] = end_date
            
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            
        return {"water": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
