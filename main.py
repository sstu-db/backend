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

# ===== Users and Authentication =====
# TODO: Add user authentication endpoints

# ===== Clients CRUD =====
@app.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting client creation with data: {client.model_dump()}")
        db_client = models.Client(**client.model_dump())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Successfully created client with ID: {db_client.id}")
        return db_client
    except Exception as e:
        logger.error(f"Error creating client: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients/{client_id}", response_model=schemas.Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching client with ID: {client_id}")
    client = db.get(models.Client, client_id)
    if not client:
        logger.warning(f"Client not found with ID: {client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    logger.info(f"Successfully retrieved client with ID: {client_id}")
    return client

@app.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting client update for ID: {client_id} with data: {client.model_dump()}")
    db_client = db.get(models.Client, client_id)
    if not db_client:
        logger.warning(f"Client not found with ID: {client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client.model_dump().items():
        setattr(db_client, key, value)
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info(f"Successfully updated client with ID: {client_id}")
    return db_client

@app.delete("/clients/{client_id}", response_model=schemas.MessageResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting client deletion for ID: {client_id}")
    db_client = db.get(models.Client, client_id)
    if not db_client:
        logger.warning(f"Client not found with ID: {client_id}")
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(db_client)
    db.commit()
    logger.info(f"Successfully deleted client with ID: {client_id}")
    return {"message": "Client deleted successfully"}

# ===== Trainers CRUD =====
@app.post("/trainers", response_model=schemas.Trainer)
def create_trainer(trainer: schemas.TrainerCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting trainer creation with data: {trainer.model_dump()}")
        db_trainer = models.Trainer(**trainer.model_dump())
        db.add(db_trainer)
        db.commit()
        db.refresh(db_trainer)
        logger.info(f"Successfully created trainer with ID: {db_trainer.id}")
        return db_trainer
    except Exception as e:
        logger.error(f"Error creating trainer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trainers/{trainer_id}", response_model=schemas.Trainer)
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching trainer with ID: {trainer_id}")
    trainer = db.get(models.Trainer, trainer_id)
    if not trainer:
        logger.warning(f"Trainer not found with ID: {trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    logger.info(f"Successfully retrieved trainer with ID: {trainer_id}")
    return trainer

@app.put("/trainers/{trainer_id}", response_model=schemas.Trainer)
def update_trainer(trainer_id: int, trainer: schemas.TrainerCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting trainer update for ID: {trainer_id} with data: {trainer.model_dump()}")
    db_trainer = db.get(models.Trainer, trainer_id)
    if not db_trainer:
        logger.warning(f"Trainer not found with ID: {trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    for key, value in trainer.model_dump().items():
        setattr(db_trainer, key, value)
    
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    logger.info(f"Successfully updated trainer with ID: {trainer_id}")
    return db_trainer

@app.delete("/trainers/{trainer_id}", response_model=schemas.MessageResponse)
def delete_trainer(trainer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting trainer deletion for ID: {trainer_id}")
    db_trainer = db.get(models.Trainer, trainer_id)
    if not db_trainer:
        logger.warning(f"Trainer not found with ID: {trainer_id}")
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    db.delete(db_trainer)
    db.commit()
    logger.info(f"Successfully deleted trainer with ID: {trainer_id}")
    return {"message": "Trainer deleted successfully"}

# ===== Trainer-Client Relationship CRUD =====
@app.get("/clients/{client_id}/trainers", response_model=schemas.TrainersResponse)
def get_client_trainers(client_id: int, db: Session = Depends(get_db)):
    """
    Получить тренеров (дата рождения, имя, фамилия, отчество) клиента.
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

@app.post("/clients/{client_id}/trainers/{trainer_id}", response_model=schemas.MessageResponse)
def add_trainer_to_client(client_id: int, trainer_id: int, db: Session = Depends(get_db)):
    """
    Добавить тренера к клиенту.
    """
    try:
        logger.info(f"Adding trainer {trainer_id} to client {client_id}")
        
        # Проверяем существование клиента и тренера
        client = db.get(models.Client, client_id)
        if not client:
            logger.warning(f"Client not found with ID: {client_id}")
            raise HTTPException(status_code=404, detail="Client not found")
            
        trainer = db.get(models.Trainer, trainer_id)
        if not trainer:
            logger.warning(f"Trainer not found with ID: {trainer_id}")
            raise HTTPException(status_code=404, detail="Trainer not found")
            
        # Проверяем, существует ли уже такая связь
        existing_link = db.exec(
            select(models.TrainerClient)
            .where(models.TrainerClient.тренер_id == trainer_id)
            .where(models.TrainerClient.клиент_id == client_id)
        ).first()
        
        if existing_link:
            logger.warning(f"Trainer {trainer_id} is already assigned to client {client_id}")
            raise HTTPException(status_code=400, detail="This trainer is already assigned to this client")
            
        # Создаем новую связь
        trainer_client = models.TrainerClient(
            тренер_id=trainer_id,
            клиент_id=client_id
        )
        
        db.add(trainer_client)
        db.commit()
        
        logger.info(f"Successfully added trainer {trainer_id} to client {client_id}")
        return {"message": "Trainer added to client successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error adding trainer to client: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clients/{client_id}/trainers/{trainer_id}", response_model=schemas.MessageResponse)
def remove_trainer_from_client(client_id: int, trainer_id: int, db: Session = Depends(get_db)):
    """
    Удалить тренера у клиента.
    """
    try:
        logger.info(f"Removing trainer {trainer_id} from client {client_id}")
        
        # Проверяем существование связи
        trainer_client = db.exec(
            select(models.TrainerClient)
            .where(models.TrainerClient.тренер_id == trainer_id)
            .where(models.TrainerClient.клиент_id == client_id)
        ).first()
        
        if not trainer_client:
            logger.warning(f"Trainer {trainer_id} is not assigned to client {client_id}")
            raise HTTPException(status_code=404, detail="This trainer is not assigned to this client")
            
        db.delete(trainer_client)
        db.commit()
        
        logger.info(f"Successfully removed trainer {trainer_id} from client {client_id}")
        return {"message": "Trainer removed from client successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error removing trainer from client: {str(e)}")
        db.rollback()
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

# ===== Training Plans CRUD =====
@app.post("/training-plans", response_model=schemas.TrainingPlan)
def create_training_plan(plan: schemas.TrainingPlanCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting training plan creation with data: {plan.model_dump()}")
        db_plan = models.TrainingPlan(**plan.model_dump())
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        logger.info(f"Successfully created training plan with ID: {db_plan.id}")
        return db_plan
    except Exception as e:
        logger.error(f"Error creating training plan: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/training-plans/{plan_id}", response_model=schemas.TrainingPlan)
def get_training_plan(plan_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching training plan with ID: {plan_id}")
    plan = db.get(models.TrainingPlan, plan_id)
    if not plan:
        logger.warning(f"Training plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Training plan not found")
    logger.info(f"Successfully retrieved training plan with ID: {plan_id}")
    return plan

@app.put("/training-plans/{plan_id}", response_model=schemas.TrainingPlan)
def update_training_plan(plan_id: int, plan: schemas.TrainingPlanCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting training plan update for ID: {plan_id} with data: {plan.model_dump()}")
    db_plan = db.get(models.TrainingPlan, plan_id)
    if not db_plan:
        logger.warning(f"Training plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Training plan not found")
    
    for key, value in plan.model_dump().items():
        setattr(db_plan, key, value)
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    logger.info(f"Successfully updated training plan with ID: {plan_id}")
    return db_plan

@app.delete("/training-plans/{plan_id}", response_model=schemas.MessageResponse)
def delete_training_plan(plan_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting training plan deletion for ID: {plan_id}")
    db_plan = db.get(models.TrainingPlan, plan_id)
    if not db_plan:
        logger.warning(f"Training plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Training plan not found")
    
    db.delete(db_plan)
    db.commit()
    logger.info(f"Successfully deleted training plan with ID: {plan_id}")
    return {"message": "Training plan deleted successfully"}

# ===== Workouts CRUD =====
@app.post("/workouts", response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting workout creation with data: {workout.model_dump()}")
        db_workout = models.Workout(**workout.model_dump())
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        logger.info(f"Successfully created workout with ID: {db_workout.id}")
        return db_workout
    except Exception as e:
        logger.error(f"Error creating workout: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workouts/{workout_id}", response_model=schemas.Workout)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching workout with ID: {workout_id}")
    workout = db.get(models.Workout, workout_id)
    if not workout:
        logger.warning(f"Workout not found with ID: {workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    logger.info(f"Successfully retrieved workout with ID: {workout_id}")
    return workout

@app.put("/workouts/{workout_id}", response_model=schemas.Workout)
def update_workout(workout_id: int, workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting workout update for ID: {workout_id} with data: {workout.model_dump()}")
    db_workout = db.get(models.Workout, workout_id)
    if not db_workout:
        logger.warning(f"Workout not found with ID: {workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    
    for key, value in workout.model_dump().items():
        setattr(db_workout, key, value)
    
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    logger.info(f"Successfully updated workout with ID: {workout_id}")
    return db_workout

@app.delete("/workouts/{workout_id}", response_model=schemas.MessageResponse)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting workout deletion for ID: {workout_id}")
    db_workout = db.get(models.Workout, workout_id)
    if not db_workout:
        logger.warning(f"Workout not found with ID: {workout_id}")
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(db_workout)
    db.commit()
    logger.info(f"Successfully deleted workout with ID: {workout_id}")
    return {"message": "Workout deleted successfully"}

# ===== Exercises CRUD =====
@app.post("/exercises", response_model=schemas.Exercise)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting exercise creation with data: {exercise.model_dump()}")
        db_exercise = models.Exercise(**exercise.model_dump())
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        logger.info(f"Successfully created exercise with ID: {db_exercise.id}")
        return db_exercise
    except Exception as e:
        logger.error(f"Error creating exercise: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercises/{exercise_id}", response_model=schemas.Exercise)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching exercise with ID: {exercise_id}")
    exercise = db.get(models.Exercise, exercise_id)
    if not exercise:
        logger.warning(f"Exercise not found with ID: {exercise_id}")
        raise HTTPException(status_code=404, detail="Exercise not found")
    logger.info(f"Successfully retrieved exercise with ID: {exercise_id}")
    return exercise

@app.put("/exercises/{exercise_id}", response_model=schemas.Exercise)
def update_exercise(exercise_id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting exercise update for ID: {exercise_id} with data: {exercise.model_dump()}")
    db_exercise = db.get(models.Exercise, exercise_id)
    if not db_exercise:
        logger.warning(f"Exercise not found with ID: {exercise_id}")
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    for key, value in exercise.model_dump().items():
        setattr(db_exercise, key, value)
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    logger.info(f"Successfully updated exercise with ID: {exercise_id}")
    return db_exercise

@app.delete("/exercises/{exercise_id}", response_model=schemas.MessageResponse)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting exercise deletion for ID: {exercise_id}")
    db_exercise = db.get(models.Exercise, exercise_id)
    if not db_exercise:
        logger.warning(f"Exercise not found with ID: {exercise_id}")
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(db_exercise)
    db.commit()
    logger.info(f"Successfully deleted exercise with ID: {exercise_id}")
    return {"message": "Exercise deleted successfully"}

# ===== Health Tracking CRUD =====
@app.post("/steps", response_model=schemas.Steps)
def create_steps(steps: schemas.StepsCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting steps record creation with data: {steps.model_dump()}")
        db_steps = models.Steps(**steps.model_dump())
        db.add(db_steps)
        db.commit()
        db.refresh(db_steps)
        logger.info(f"Successfully created steps record with ID: {db_steps.id}")
        return db_steps
    except Exception as e:
        logger.error(f"Error creating steps record: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/steps/{steps_id}", response_model=schemas.Steps)
def get_steps(steps_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching steps record with ID: {steps_id}")
    steps = db.get(models.Steps, steps_id)
    if not steps:
        logger.warning(f"Steps record not found with ID: {steps_id}")
        raise HTTPException(status_code=404, detail="Steps record not found")
    logger.info(f"Successfully retrieved steps record with ID: {steps_id}")
    return steps

@app.put("/steps/{steps_id}", response_model=schemas.Steps)
def update_steps(steps_id: int, steps: schemas.StepsCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting steps record update for ID: {steps_id} with data: {steps.model_dump()}")
    db_steps = db.get(models.Steps, steps_id)
    if not db_steps:
        logger.warning(f"Steps record not found with ID: {steps_id}")
        raise HTTPException(status_code=404, detail="Steps record not found")
    
    for key, value in steps.model_dump().items():
        setattr(db_steps, key, value)
    
    db.add(db_steps)
    db.commit()
    db.refresh(db_steps)
    logger.info(f"Successfully updated steps record with ID: {steps_id}")
    return db_steps

@app.delete("/steps/{steps_id}", response_model=schemas.MessageResponse)
def delete_steps(steps_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting steps record deletion for ID: {steps_id}")
    db_steps = db.get(models.Steps, steps_id)
    if not db_steps:
        logger.warning(f"Steps record not found with ID: {steps_id}")
        raise HTTPException(status_code=404, detail="Steps record not found")
    
    db.delete(db_steps)
    db.commit()
    logger.info(f"Successfully deleted steps record with ID: {steps_id}")
    return {"message": "Steps record deleted successfully"}

@app.post("/water", response_model=schemas.Water)
def create_water(water: schemas.WaterCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting water record creation with data: {water.model_dump()}")
        db_water = models.Water(**water.model_dump())
        db.add(db_water)
        db.commit()
        db.refresh(db_water)
        logger.info(f"Successfully created water record with ID: {db_water.id}")
        return db_water
    except Exception as e:
        logger.error(f"Error creating water record: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/water/{water_id}", response_model=schemas.Water)
def get_water(water_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching water record with ID: {water_id}")
    water = db.get(models.Water, water_id)
    if not water:
        logger.warning(f"Water record not found with ID: {water_id}")
        raise HTTPException(status_code=404, detail="Water record not found")
    logger.info(f"Successfully retrieved water record with ID: {water_id}")
    return water

@app.put("/water/{water_id}", response_model=schemas.Water)
def update_water(water_id: int, water: schemas.WaterCreate, db: Session = Depends(get_db)):
    logger.info(f"Starting water record update for ID: {water_id} with data: {water.model_dump()}")
    db_water = db.get(models.Water, water_id)
    if not db_water:
        logger.warning(f"Water record not found with ID: {water_id}")
        raise HTTPException(status_code=404, detail="Water record not found")
    
    for key, value in water.model_dump().items():
        setattr(db_water, key, value)
    
    db.add(db_water)
    db.commit()
    db.refresh(db_water)
    logger.info(f"Successfully updated water record with ID: {water_id}")
    return db_water

@app.delete("/water/{water_id}", response_model=schemas.MessageResponse)
def delete_water(water_id: int, db: Session = Depends(get_db)):
    logger.info(f"Starting water record deletion for ID: {water_id}")
    db_water = db.get(models.Water, water_id)
    if not db_water:
        logger.warning(f"Water record not found with ID: {water_id}")
        raise HTTPException(status_code=404, detail="Water record not found")
    
    db.delete(db_water)
    db.commit()
    logger.info(f"Successfully deleted water record with ID: {water_id}")
    return {"message": "Water record deleted successfully"}

# ===== Diaries CRUD =====
@app.post("/diaries", response_model=schemas.Diary)
def create_diary(diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting diary creation for user {diary.пользователь_id}")
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
            logger.info(f"Adding feelings to diary: {diary.feelings}")
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        if diary.feeling_reasons:
            logger.info(f"Adding feeling reasons to diary: {diary.feeling_reasons}")
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

@app.get("/diaries/{diary_id}", response_model=schemas.Diary)
def get_diary(diary_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching diary with ID: {diary_id}")
    diary = db.get(models.Diary, diary_id)
    if not diary:
        logger.warning(f"Diary not found with ID: {diary_id}")
        raise HTTPException(status_code=404, detail="Diary not found")
    logger.info(f"Successfully retrieved diary with ID: {diary_id}")
    return diary

@app.put("/diaries/{diary_id}", response_model=schemas.Diary)
def update_diary(diary_id: int, diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting diary update for ID: {diary_id}")
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
            logger.info(f"Updating feelings for diary: {diary.feelings}")
            feelings = db.exec(select(models.Feeling).where(models.Feeling.id.in_(diary.feelings))).all()
            db_diary.feelings = feelings
            
        if diary.feeling_reasons is not None:
            logger.info(f"Updating feeling reasons for diary: {diary.feeling_reasons}")
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
    try:
        logger.info(f"Starting diary deletion for ID: {diary_id}")
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

# ===== Feelings and Reasons CRUD =====
@app.get("/feelings", response_model=List[schemas.Feeling])
def get_feelings(db: Session = Depends(get_db)):
    """
    Получить список всех чувств.
    """
    try:
        logger.info("Fetching all feelings")
        statement = select(models.Feeling)
        feelings = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(feelings)} feelings")
        return feelings
    except Exception as e:
        logger.error(f"Error fetching feelings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feeling-reasons", response_model=List[schemas.FeelingReason])
def get_feeling_reasons(db: Session = Depends(get_db)):
    """
    Получить список всех причин чувств.
    """
    try:
        logger.info("Fetching all feeling reasons")
        statement = select(models.FeelingReason)
        feeling_reasons = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(feeling_reasons)} feeling reasons")
        return feeling_reasons
    except Exception as e:
        logger.error(f"Error fetching feeling reasons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
