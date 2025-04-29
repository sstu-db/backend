from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date, datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

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

@app.get("/tables", response_model=schemas.TablesResponse)
def get_tables():
    """
    Возвращает список таблиц в базе данных.
    """
    try:
        logger.info("Fetching list of tables")
        tables = [table.__tablename__ for table in models.SQLModel.__subclasses__() if hasattr(table, '__tablename__')]
        logger.info(f"Successfully retrieved {len(tables)} tables")
        return {"data": tables}
    except Exception as e:
        logger.error(f"Error fetching tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tables/{table_name}", response_model=schemas.TableInfoResponse)
def get_table_info(table_name: str):
    """
    Возвращает информацию о колонках указанной таблицы.
    """
    try:
        logger.info(f"Fetching info for table: {table_name}")
        model = next((table for table in models.SQLModel.__subclasses__() 
                     if hasattr(table, '__tablename__') and table.__tablename__ == table_name), None)
        if not model:
            logger.warning(f"Table not found: {table_name}")
            raise HTTPException(status_code=404, detail="Table not found")
            
        columns_info = [
            {"name": field_name, "type": str(field.type_)} 
            for field_name, field in model.__fields__.items()
        ]
        logger.info(f"Successfully retrieved info for table {table_name} with {len(columns_info)} columns")
        return {"table": table_name, "data": columns_info}
    except Exception as e:
        logger.error(f"Error fetching table info for {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=schemas.QueryResponse)
def execute_query(query_request: schemas.QueryRequest):
    """
    Выполняет SQL-запрос, переданный в теле запроса.
    """
    query_str = query_request.query
    try:
        logger.info(f"Executing query: {query_str}")
        with Session(engine) as session:
            result = session.execute(text(query_str))
            columns = result.keys() if result.returns_rows else []
            rows = [dict(zip(columns, row)) for row in result.fetchall()] if result.returns_rows else []
        logger.info(f"Query executed successfully, returned {len(rows)} rows")
        return {"data": rows}
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients/{client_id}/trainers", response_model=schemas.TrainersResponse)
def get_client_trainers(client_id: int, db: Session = Depends(get_db)):
    """
    Получить тренеров (дата рождения, имя, фамилия, отчество, специальности) клиента.
    """
    try:
        logger.info(f"Fetching trainers for client ID: {client_id}")
        client = db.get(models.Client, client_id)
        if not client:
            logger.warning(f"Client not found with ID: {client_id}")
            raise HTTPException(status_code=404, detail="Client not found")
            
        # Join with User table and TrainerClient table to get user data
        statement = (
            select(models.Trainer)
            .join(models.User, models.Trainer.пользователь_id == models.User.id)
            .join(models.TrainerClient, models.Trainer.id == models.TrainerClient.тренер_id)
            .where(models.TrainerClient.клиент_id == client_id)
        )
        trainers = db.exec(statement).all()
        
        # Convert to response models to break cyclic references
        trainer_responses = [
            schemas.TrainerResponse(
                id=trainer.id,
                пользователь_id=trainer.пользователь_id,
                user=trainer.user
            )
            for trainer in trainers
        ]
        
        logger.info(f"Successfully retrieved {len(trainers)} trainers for client {client_id}")
        return {"data": trainer_responses}
    except Exception as e:
        logger.error(f"Error fetching trainers for client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trainers/{trainer_id}/clients", response_model=schemas.ClientsResponse)
def get_trainer_clients(trainer_id: int, db: Session = Depends(get_db)):
    """
    Получить клиентов (дата рождения, имя, фамилия, отчество, цель тренировок, уровень подготовки) тренера.
    """
    try:
        logger.info(f"Fetching clients for trainer ID: {trainer_id}")
        trainer = db.get(models.Trainer, trainer_id)
        if not trainer:
            logger.warning(f"Trainer not found with ID: {trainer_id}")
            raise HTTPException(status_code=404, detail="Trainer not found")
            
        # Join with User table, TrainerClient table, and PreparationLevel table
        statement = (
            select(models.Client)
            .join(models.User, models.Client.пользователь_id == models.User.id)
            .join(models.TrainerClient, models.Client.id == models.TrainerClient.клиент_id)
            .join(models.PreparationLevel, models.Client.уровень_подготовки_id == models.PreparationLevel.id)
            .where(models.TrainerClient.тренер_id == trainer_id)
        )
        clients = db.exec(statement).all()
        
        logger.info(f"Successfully retrieved {len(clients)} clients for trainer {trainer_id}")
        return {"data": clients}
    except Exception as e:
        logger.error(f"Error fetching clients for trainer {trainer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/training-plans", response_model=schemas.TrainingPlansResponse)
def get_training_plans(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Получить план тренировок (название, описание, тренировки) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        statement = select(models.TrainingPlan)
        
        if client_id:
            client = db.get(models.Client, client_id)
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            statement = statement.where(models.TrainingPlanUser.пользователь_id == client.пользователь_id)
            
        if trainer_id:
            trainer = db.get(models.Trainer, trainer_id)
            if not trainer:
                raise HTTPException(status_code=404, detail="Trainer not found")
            statement = statement.where(models.TrainingPlanUser.пользователь_id == trainer.пользователь_id)
            
        return {"data": db.exec(statement).all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workouts", response_model=schemas.WorkoutsResponse)
def get_workouts(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Получить тренировки (название, формат проведения, время начала, вид тренировки, упражнения) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        logger.info(f"Starting get_workouts request with client_id={client_id}, trainer_id={trainer_id}")
        
        # Base query with joins for exercises
        statement = (
            select(models.Workout)
            .join(models.WorkoutExercise, models.Workout.id == models.WorkoutExercise.тренировка_id)
            .join(models.Exercise, models.WorkoutExercise.упражнение_id == models.Exercise.id)
        )
        logger.debug("Initial statement with exercise joins created")
        
        if client_id:
            logger.info(f"Fetching client with ID: {client_id}")
            client = db.get(models.Client, client_id)
            if not client:
                logger.warning(f"Client not found with ID: {client_id}")
                raise HTTPException(status_code=404, detail="Client not found")
            logger.info(f"Found client with user_id: {client.пользователь_id}")
            
            statement = (
                select(models.Workout)
                .join(models.WorkoutUser, models.Workout.id == models.WorkoutUser.тренировка_id)
                .join(models.WorkoutExercise, models.Workout.id == models.WorkoutExercise.тренировка_id)
                .join(models.Exercise, models.WorkoutExercise.упражнение_id == models.Exercise.id)
                .where(models.WorkoutUser.пользователь_id == client.пользователь_id)
            )
            logger.debug("Statement updated for client workouts with exercises")
            
        if trainer_id:
            logger.info(f"Fetching trainer with ID: {trainer_id}")
            trainer = db.get(models.Trainer, trainer_id)
            if not trainer:
                logger.warning(f"Trainer not found with ID: {trainer_id}")
                raise HTTPException(status_code=404, detail="Trainer not found")
            logger.info(f"Found trainer with user_id: {trainer.пользователь_id}")
            
            statement = (
                select(models.Workout)
                .join(models.WorkoutUser, models.Workout.id == models.WorkoutUser.тренировка_id)
                .join(models.WorkoutExercise, models.Workout.id == models.WorkoutExercise.тренировка_id)
                .join(models.Exercise, models.WorkoutExercise.упражнение_id == models.Exercise.id)
                .where(models.WorkoutUser.пользователь_id == trainer.пользователь_id)
            )
            logger.debug("Statement updated for trainer workouts with exercises")
            
        logger.info("Executing final query")
        workouts = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(workouts)} workouts with their exercises")
        
        # Load exercises for each workout
        for workout in workouts:
            workout.exercises = db.exec(
                select(models.Exercise)
                .join(models.WorkoutExercise, models.Exercise.id == models.WorkoutExercise.упражнение_id)
                .where(models.WorkoutExercise.тренировка_id == workout.id)
            ).all()
            logger.debug(f"Loaded {len(workout.exercises)} exercises for workout {workout.id}")
        
        return {"data": workouts}
    except HTTPException as he:
        logger.error(f"HTTP Exception in get_workouts: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in get_workouts: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercises", response_model=schemas.ExercisesResponse)
def get_exercises(
    client_id: Optional[int] = None,
    trainer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Получить упражнения (название, тип, уровень сложности, описание, мышцы с указанием важности этой мышцы в упражнении, снаряжение) клиента, либо тренера, либо по клиента и тренера.
    """
    try:
        statement = select(models.Exercise)
        
        if client_id:
            client = db.get(models.Client, client_id)
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            statement = (
                select(models.Exercise)
                .join(models.ExerciseUser, models.Exercise.id == models.ExerciseUser.упражнение_id)
                .where(models.ExerciseUser.пользователь_id == client.пользователь_id)
            )
            
        if trainer_id:
            trainer = db.get(models.Trainer, trainer_id)
            if not trainer:
                raise HTTPException(status_code=404, detail="Trainer not found")
            statement = (
                select(models.Exercise)
                .join(models.ExerciseUser, models.Exercise.id == models.ExerciseUser.упражнение_id)
                .where(models.ExerciseUser.пользователь_id == trainer.пользователь_id)
            )
            
        return {"data": db.exec(statement).all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/steps", response_model=schemas.StepsResponse)
def get_steps(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Получить шаги (количество шагов, цель шагов, дата записи) по пользователю и диапазону дат.
    """
    try:
        statement = select(models.Steps).where(models.Steps.пользователь_id == user_id)
        
        if start_date:
            statement = statement.where(models.Steps.дата >= start_date)
            
        if end_date:
            statement = statement.where(models.Steps.дата <= end_date)
            
        return {"data": db.exec(statement).all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/water", response_model=schemas.WaterResponse)
def get_water(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Получить потребление воды (объем выпитой воды, цель, дата) по пользователю и диапазону дат.
    """
    try:
        statement = select(models.Water).where(models.Water.пользователь_id == user_id)
        
        if start_date:
            statement = statement.where(models.Water.дата >= start_date)
            
        if end_date:
            statement = statement.where(models.Water.дата <= end_date)
            
        return {"data": db.exec(statement).all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        logger.info(f"Fetching diaries for user {user_id} from {start_date} to {end_date}")
        statement = select(models.Diary).where(models.Diary.пользователь_id == user_id)
        
        if start_date:
            statement = statement.where(models.Diary.дата >= start_date)
            
        if end_date:
            statement = statement.where(models.Diary.дата <= end_date)
            
        diaries = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(diaries)} diaries for user {user_id}")
        return {"data": diaries}
    except Exception as e:
        logger.error(f"Error fetching diaries for user {user_id}: {str(e)}")
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
        logger.info(f"Creating new diary for user {diary.пользователь_id}")
        user = db.get(models.User, diary.пользователь_id)
        if not user:
            logger.warning(f"User not found with ID: {diary.пользователь_id}")
            raise HTTPException(status_code=404, detail="User not found")
            
        diary_data = diary.model_dump(exclude={'feelings', 'feeling_reasons'})
        db_diary = models.Diary(**diary_data)
        
        db.add(db_diary)
        db.commit()
        db.refresh(db_diary)
        
        if diary.feelings:
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        if diary.feeling_reasons:
            feeling_reasons = db.exec(select(models.FeelingReason).where(models.FeelingReason.id.in_(diary.feeling_reasons))).all()
            db_diary.feeling_reasons = feeling_reasons
            
        db.commit()
        
        statement = select(models.Diary).where(models.Diary.id == db_diary.id)
        db_diary = db.exec(statement).first()
        
        logger.info(f"Successfully created diary with ID: {db_diary.id}")
        return db_diary
    except Exception as e:
        logger.error(f"Error creating diary: {str(e)}")
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
        logger.info(f"Updating diary with ID: {diary_id}")
        db_diary = db.get(models.Diary, diary_id)
        if not db_diary:
            logger.warning(f"Diary not found with ID: {diary_id}")
            raise HTTPException(status_code=404, detail="Diary not found")
            
        user = db.get(models.User, diary.пользователь_id)
        if not user:
            logger.warning(f"User not found with ID: {diary.пользователь_id}")
            raise HTTPException(status_code=404, detail="User not found")
            
        diary_data = diary.model_dump(exclude={'feelings', 'feeling_reasons'})
        for key, value in diary_data.items():
            setattr(db_diary, key, value)
        
        db.add(db_diary)
        db.commit()
        db.refresh(db_diary)
        
        if diary.feelings is not None:
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        if diary.feeling_reasons is not None:
            feeling_reasons = db.exec(select(models.FeelingReason).where(models.FeelingReason.id.in_(diary.feeling_reasons))).all()
            db_diary.feeling_reasons = feeling_reasons
        
        db.add(db_diary)
        db.commit()
        
        statement = select(models.Diary).where(models.Diary.id == diary_id)
        db_diary = db.exec(statement).first()
        
        logger.info(f"Successfully updated diary with ID: {diary_id}")
        return db_diary
    except Exception as e:
        logger.error(f"Error updating diary {diary_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/diaries/{diary_id}", response_model=schemas.MessageResponse)
def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    """
    Удалить дневник.
    """
    try:
        logger.info(f"Deleting diary with ID: {diary_id}")
        db_diary = db.get(models.Diary, diary_id)
        if not db_diary:
            logger.warning(f"Diary not found with ID: {diary_id}")
            raise HTTPException(status_code=404, detail="Diary not found")
            
        db.delete(db_diary)
        db.commit()
        
        logger.info(f"Successfully deleted diary with ID: {diary_id}")
        return {"message": "Diary deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting diary {diary_id}: {str(e)}")
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
