from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date, datetime

from database import get_db
import models
import schemas

# Настройте параметры подключения к PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/app"

app = FastAPI()

# Разрешаем CORS (настройте список allowed origins по необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/tables", response_model=schemas.TablesResponse)
# def get_tables():
#     """
#     Возвращает список таблиц в базе данных.
#     """
#     try:
#         tables = [table.__tablename__ for table in models.SQLModel.__subclasses__() if hasattr(table, '__tablename__')]
#         return {"data": tables}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/tables/{table_name}", response_model=schemas.TableInfoResponse)
# def get_table_info(table_name: str):
#     """
#     Возвращает информацию о колонках указанной таблицы.
#     """
#     try:
#         model = next((table for table in models.SQLModel.__subclasses__() 
#                      if hasattr(table, '__tablename__') and table.__tablename__ == table_name), None)
#         if not model:
#             raise HTTPException(status_code=404, detail="Table not found")
            
#         columns_info = [
#             {"name": field_name, "type": str(field.type_)} 
#             for field_name, field in model.__fields__.items()
#         ]
#         return {"table": table_name, "data": columns_info}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/query", response_model=schemas.QueryResponse)
# def execute_query(query_request: schemas.QueryRequest):
#     """
#     Выполняет SQL-запрос, переданный в теле запроса.
#     """
#     query_str = query_request.query
#     try:
#         with Session(engine) as session:
#             result = session.execute(text(query_str))
#             columns = result.keys() if result.returns_rows else []
#             rows = [dict(zip(columns, row)) for row in result.fetchall()] if result.returns_rows else []
#         return {"data": rows}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/clients/{client_id}/trainers", response_model=schemas.TrainersResponse)
# def get_client_trainers(client_id: int, db: Session = Depends(get_db)):
#     """
#     Получить тренеров (дата рождения, имя, фамилия, отчество, специальности) клиента.
#     """
#     try:
#         client = db.get(models.Client, client_id)
#         if not client:
#             raise HTTPException(status_code=404, detail="Client not found")
            
#         # Load trainers with their user information and specialties
#         statement = select(models.Trainer).where(models.TrainerClient.клиент_id == client_id)
#         trainers = db.exec(statement).all()
        
#         return {"data": trainers}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/trainers/{trainer_id}/clients", response_model=schemas.ClientsResponse)
# def get_trainer_clients(trainer_id: int, db: Session = Depends(get_db)):
#     """
#     Получить клиентов (дата рождения, имя, фамилия, отчество, цель тренировок, уровень подготовки) тренера.
#     """
#     try:
#         trainer = db.get(models.Trainer, trainer_id)
#         if not trainer:
#             raise HTTPException(status_code=404, detail="Trainer not found")
            
#         # Load clients with their user information, training goals, and preparation level
#         statement = select(models.Client).where(models.TrainerClient.тренер_id == trainer_id)
#         clients = db.exec(statement).all()
        
#         return {"data": clients}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/training-plans", response_model=schemas.TrainingPlansResponse)
# def get_training_plans(
#     client_id: Optional[int] = None,
#     trainer_id: Optional[int] = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     Получить план тренировок (название, описание, тренировки) клиента, либо тренера, либо по клиента и тренера.
#     """
#     try:
#         statement = select(models.TrainingPlan)
        
#         if client_id:
#             client = db.get(models.Client, client_id)
#             if not client:
#                 raise HTTPException(status_code=404, detail="Client not found")
#             statement = statement.where(models.TrainingPlanUser.пользователь_id == client.пользователь_id)
            
#         if trainer_id:
#             trainer = db.get(models.Trainer, trainer_id)
#             if not trainer:
#                 raise HTTPException(status_code=404, detail="Trainer not found")
#             statement = statement.where(models.TrainingPlanUser.пользователь_id == trainer.пользователь_id)
            
#         return {"data": db.exec(statement).all()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/workouts", response_model=schemas.WorkoutsResponse)
# def get_workouts(
#     client_id: Optional[int] = None,
#     trainer_id: Optional[int] = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     Получить тренировки (название, формат проведения, время начала, вид тренировки, упражнения) клиента, либо тренера, либо по клиента и тренера.
#     """
#     try:
#         statement = select(models.Workout)
        
#         if client_id:
#             client = db.get(models.Client, client_id)
#             if not client:
#                 raise HTTPException(status_code=404, detail="Client not found")
#             statement = statement.where(models.WorkoutUser.пользователь_id == client.пользователь_id)
            
#         if trainer_id:
#             trainer = db.get(models.Trainer, trainer_id)
#             if not trainer:
#                 raise HTTPException(status_code=404, detail="Trainer not found")
#             statement = statement.where(models.WorkoutUser.пользователь_id == trainer.пользователь_id)
            
#         return {"data": db.exec(statement).all()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/exercises", response_model=schemas.ExercisesResponse)
# def get_exercises(
#     client_id: Optional[int] = None,
#     trainer_id: Optional[int] = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     Получить упражнения (название, тип, уровень сложности, описание, мышцы с указанием важности этой мышцы в упражнении, снаряжение) клиента, либо тренера, либо по клиента и тренера.
#     """
#     try:
#         statement = select(models.Exercise)
        
#         if client_id:
#             client = db.get(models.Client, client_id)
#             if not client:
#                 raise HTTPException(status_code=404, detail="Client not found")
#             statement = statement.where(models.ExerciseUser.пользователь_id == client.пользователь_id)
            
#         if trainer_id:
#             trainer = db.get(models.Trainer, trainer_id)
#             if not trainer:
#                 raise HTTPException(status_code=404, detail="Trainer not found")
#             statement = statement.where(models.ExerciseUser.пользователь_id == trainer.пользователь_id)
            
#         return {"data": db.exec(statement).all()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/steps", response_model=schemas.StepsResponse)
# def get_steps(
#     user_id: int,
#     start_date: Optional[date] = None,
#     end_date: Optional[date] = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     Получить шаги (количество шагов, цель шагов, дата записи) по пользователю и диапазону дат.
#     """
#     try:
#         statement = select(models.Steps).where(models.Steps.пользователь_id == user_id)
        
#         if start_date:
#             statement = statement.where(models.Steps.дата >= start_date)
            
#         if end_date:
#             statement = statement.where(models.Steps.дата <= end_date)
            
#         return {"data": db.exec(statement).all()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/water", response_model=schemas.WaterResponse)
# def get_water(
#     user_id: int,
#     start_date: Optional[date] = None,
#     end_date: Optional[date] = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     Получить потребление воды (объем выпитой воды, цель, дата) по пользователю и диапазону дат.
#     """
#     try:
#         statement = select(models.Water).where(models.Water.пользователь_id == user_id)
        
#         if start_date:
#             statement = statement.where(models.Water.дата >= start_date)
            
#         if end_date:
#             statement = statement.where(models.Water.дата <= end_date)
            
#         return {"data": db.exec(statement).all()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/diaries", response_model=schemas.DiariesResponse)
def get_diaries(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Получить дневники состояния (дата записи, текстовая заметка, файл) по пользователю и диапазону дат.
    """
    try:
        statement = select(models.Diary).where(models.Diary.пользователь_id == user_id)
        
        if start_date:
            statement = statement.where(models.Diary.дата >= start_date)
            
        if end_date:
            statement = statement.where(models.Diary.дата <= end_date)
            
        return {"data": db.exec(statement).all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diaries", response_model=schemas.Diary)
def create_diary(
    diary: schemas.DiaryCreate,
    db: Session = Depends(get_db)
):
    """
    Создать дневник.
    """
    try:
        user = db.get(models.User, diary.пользователь_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Create diary without relationships first
        diary_data = diary.model_dump(exclude={'feelings', 'feeling_reasons'})
        db_diary = models.Diary(**diary_data)
        
        db.add(db_diary)
        db.commit()
        db.refresh(db_diary)
        
        # Add feelings if provided
        if diary.feelings:
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        # Add feeling reasons if provided
        if diary.feeling_reasons:
            feeling_reasons = db.exec(select(models.FeelingReason).where(models.FeelingReason.id.in_(diary.feeling_reasons))).all()
            db_diary.feeling_reasons = feeling_reasons
            
        db.commit()
        
        # Reload with relationships
        statement = select(models.Diary).where(models.Diary.id == db_diary.id)
        db_diary = db.exec(statement).first()
        
        return db_diary
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/diaries/{diary_id}", response_model=schemas.Diary)
def update_diary(
    diary_id: int,
    diary: schemas.DiaryCreate,
    db: Session = Depends(get_db)
):
    """
    Обновить дневник.
    """
    try:
        db_diary = db.get(models.Diary, diary_id)
        if not db_diary:
            raise HTTPException(status_code=404, detail="Diary not found")
            
        # Проверяем существование пользователя
        user = db.get(models.User, diary.пользователь_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Update basic fields first
        diary_data = diary.model_dump(exclude={'feelings', 'feeling_reasons'})
        for key, value in diary_data.items():
            setattr(db_diary, key, value)
        
        db.add(db_diary)
        db.commit()
        db.refresh(db_diary)
        
        # Update feelings if provided
        if diary.feelings is not None:
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        # Update feeling reasons if provided
        if diary.feeling_reasons is not None:
            feeling_reasons = db.exec(select(models.FeelingReason).where(models.FeelingReason.id.in_(diary.feeling_reasons))).all()
            db_diary.feeling_reasons = feeling_reasons
        
        db.add(db_diary)
        db.commit()
        
        # Reload with relationships
        statement = select(models.Diary).where(models.Diary.id == diary_id)
        db_diary = db.exec(statement).first()
        
        return db_diary
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/diaries/{diary_id}", response_model=schemas.MessageResponse)
def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    """
    Удалить дневник.
    """
    try:
        db_diary = db.get(models.Diary, diary_id)
        if not db_diary:
            raise HTTPException(status_code=404, detail="Diary not found")
            
        db.delete(db_diary)
        db.commit()
        
        return {"message": "Diary deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feelings", response_model=List[schemas.Feeling])
def get_feelings(db: Session = Depends(get_db)):
    """
    Получить список всех чувств.
    """
    try:
        statement = select(models.Feeling)
        feelings = db.exec(statement).all()
        return feelings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feeling-reasons", response_model=List[schemas.FeelingReason])
def get_feeling_reasons(db: Session = Depends(get_db)):
    """
    Получить список всех причин чувств.
    """
    try:
        statement = select(models.FeelingReason)
        feeling_reasons = db.exec(statement).all()
        return feeling_reasons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
