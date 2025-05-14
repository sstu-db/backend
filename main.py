from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import date
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
import auth


app = FastAPI()

# Разрешаем CORS (настройте список allowed origins по необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Authentication Endpoints =====
@app.post("/register/client", response_model=schemas.Token)
async def register_client(user_data: schemas.ClientRegister, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting client registration with email: {user_data.почта}")
        
        # Check if user already exists
        existing_user = db.exec(
            select(models.User).where(models.User.почта == user_data.почта)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user_dict = user_data.model_dump()
        db_user = models.User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create client
        client = models.Client(
            пользователь_id=db_user.id,
            уровень_подготовки_id=user_data.уровень_подготовки_id
        )
        db.add(client)
        
        # Add training goals to client
        if user_data.training_goals:
            for goal_id in user_data.training_goals:
                goal = db.get(models.TrainingGoal, goal_id)
                if not goal:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Training goal with ID {goal_id} not found"
                    )
                client.training_goals.append(goal)
        
        # Add training types to client
        if user_data.training_types:
            for type_id in user_data.training_types:
                training_type = db.get(models.TrainingType, type_id)
                if not training_type:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Training type with ID {type_id} not found"
                    )
                client.training_types.append(training_type)
        
        db.commit()
        
        logger.info(f"Successfully registered client with ID: {db_user.id}")
        return {"access_token": db_user.почта, "token_type": "bearer"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during client registration: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register/trainer", response_model=schemas.Token)
async def register_trainer(user_data: schemas.TrainerRegister, db: Session = Depends(get_db)):
    try:
        logger.info(f"Starting trainer registration with email: {user_data.почта}")
        
        # Check if user already exists
        existing_user = db.exec(
            select(models.User).where(models.User.почта == user_data.почта)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user_dict = user_data.model_dump() # In a real app, hash the password
        db_user = models.User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create trainer
        trainer = models.Trainer(пользователь_id=db_user.id)
        db.add(trainer)
        
        # Add specialties to trainer
        if user_data.specialties:
            for specialty_id in user_data.specialties:
                specialty = db.get(models.TrainerSpecialty, specialty_id)
                if not specialty:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Specialty with ID {specialty_id} not found"
                    )
                trainer.specialties.append(specialty)
        
        db.commit()
        
        logger.info(f"Successfully registered trainer with ID: {db_user.id}")
        return {"access_token": db_user.почта, "token_type": "bearer"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during trainer registration: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # Ищем пользователя по email
        user = db.exec(select(models.User).where(models.User.почта == form_data.username)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Проверяем пароль
        if not auth.verify_password(form_data.password, user.хэш_пароля):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"access_token": user.почта, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error fetching current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Trainer-Client Relationship CRUD =====
@app.get("/my-trainers", response_model=schemas.ClientTrainersResponse)
def get_my_trainers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить тренеров (дата рождения, имя, фамилия, отчество, специальности) текущего пользователя.
    """
    try:
        logger.info(f"Fetching trainers for current user {current_user.id}")
        
        # Получаем клиента текущего пользователя
        client = db.exec(
            select(models.Client)
            .where(models.Client.пользователь_id == current_user.id)
        ).first()
        
        if not client:
            logger.warning(f"Client not found for user ID: {current_user.id}")
            raise HTTPException(status_code=404, detail="Client not found")
            
        statement = (
            select(models.Trainer)
            .join(models.User, models.Trainer.пользователь_id == models.User.id)
            .join(models.TrainerClient, models.Trainer.id == models.TrainerClient.тренер_id)
            .where(models.TrainerClient.клиент_id == client.id)
            .options(
                selectinload(models.Trainer.user),
                selectinload(models.Trainer.specialties)
            )
        )
        trainers = db.exec(statement).all()
        
        logger.info(f"Successfully retrieved {len(trainers)} trainers for current user")
        return {"data": trainers}
    except Exception as e:
        logger.error(f"Error fetching trainers for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/my-clients", response_model=schemas.TrainerClientsResponse)
def get_my_clients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить клиентов (дата рождения, имя, фамилия, отчество, цель тренировок, уровень подготовки) текущего пользователя-тренера.
    """
    try:
        logger.info(f"Fetching clients for current trainer user {current_user.id}")
        
        # Получаем тренера текущего пользователя
        trainer = db.exec(
            select(models.Trainer)
            .where(models.Trainer.пользователь_id == current_user.id)
        ).first()
        
        if not trainer:
            logger.warning(f"Trainer not found for user ID: {current_user.id}")
            raise HTTPException(status_code=404, detail="Trainer not found")
            
        statement = (
            select(models.Client)
            .join(models.User, models.Client.пользователь_id == models.User.id)
            .join(models.TrainerClient, models.Client.id == models.TrainerClient.клиент_id)
            .join(models.PreparationLevel, models.Client.уровень_подготовки_id == models.PreparationLevel.id)
            .where(models.TrainerClient.тренер_id == trainer.id)
        )
        clients = db.exec(statement).all()
        
        logger.info(f"Successfully retrieved {len(clients)} clients for current trainer")
        return {"data": clients}
    except Exception as e:
        logger.error(f"Error fetching clients for current trainer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clients/{client_id}/trainers/{trainer_id}", response_model=schemas.MessageResponse)
def add_trainer_to_client(
    client_id: int,
    trainer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Adding trainer {trainer_id} to client {client_id}")
        
        client = db.get(models.Client, client_id)
        if not client:
            logger.warning(f"Client not found with ID: {client_id}")
            raise HTTPException(status_code=404, detail="Client not found")

        # Check if current user is a client
        current_client = db.exec(
            select(models.Client)
            .where(models.Client.пользователь_id == current_user.id)
        ).first()
        
        # Check if current user is a trainer
        current_trainer = db.exec(
            select(models.Trainer)
            .where(models.Trainer.пользователь_id == current_user.id)
        ).first()

        if current_client and current_trainer:
            pass
        # If current user is a client, check if they own the client record
        elif current_client and current_client.id != client_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this client")
        # If current user is a trainer, check if they are assigned to this client
        elif current_trainer and current_trainer.id != trainer_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this client")
            
        trainer = db.get(models.Trainer, trainer_id)
        if not trainer:
            logger.warning(f"Trainer not found with ID: {trainer_id}")
            raise HTTPException(status_code=404, detail="Trainer not found")
            
        existing_link = db.exec(
            select(models.TrainerClient)
            .where(models.TrainerClient.тренер_id == trainer_id)
            .where(models.TrainerClient.клиент_id == client_id)
        ).first()
        
        if existing_link:
            logger.warning(f"Trainer {trainer_id} is already assigned to client {client_id}")
            raise HTTPException(status_code=400, detail="This trainer is already assigned to this client")
            
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
def remove_trainer_from_client(
    client_id: int,
    trainer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Removing trainer {trainer_id} from client {client_id}")
        
        client = db.get(models.Client, client_id)
        if not client:
            logger.warning(f"Client not found with ID: {client_id}")
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Check if current user is a client
        current_client = db.exec(
            select(models.Client)
            .where(models.Client.пользователь_id == current_user.id)
        ).first()
        
        # Check if current user is a trainer
        current_trainer = db.exec(
            select(models.Trainer)
            .where(models.Trainer.пользователь_id == current_user.id)
        ).first()
        # Check if the client belongs to the current user
        if current_client and current_trainer:
            pass
        # If current user is a client, check if they own the client record
        elif current_client and current_client.id != client_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this client")
        # If current user is a trainer, check if they are assigned to this client
        elif current_trainer and current_trainer.id != trainer_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this client")
        
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

@app.get("/trainers", response_model=List[schemas.Trainer])
def get_all_trainers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить список всех тренеров с их пользовательской информацией и специальностями.
    """
    try:
        logger.info("Fetching all trainers")
        
        statement = (
            select(models.Trainer)
            .join(models.User, models.Trainer.пользователь_id == models.User.id)
            .options(
                selectinload(models.Trainer.user),
                selectinload(models.Trainer.specialties)
            )
        )
        
        trainers = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(trainers)} trainers")
        return trainers
    except Exception as e:
        logger.error(f"Error fetching all trainers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients", response_model=List[schemas.Client])
def get_all_clients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить список всех клиентов с их пользовательской информацией и уровнем подготовки.
    """
    try:
        logger.info("Fetching all clients")
        
        statement = (
            select(models.Client)
            .join(models.User, models.Client.пользователь_id == models.User.id)
            .join(models.PreparationLevel, models.Client.уровень_подготовки_id == models.PreparationLevel.id)
            .options(
                selectinload(models.Client.user),
                selectinload(models.Client.preparation_level),
                selectinload(models.Client.training_goals),
                selectinload(models.Client.training_types)
            )
        )
        
        clients = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(clients)} clients")
        return clients
    except Exception as e:
        logger.error(f"Error fetching all clients: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== Training Plans CRUD =====
@app.get("/my-training-plans", response_model=List[schemas.TrainingPlan])
def get_all_plans_by_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить все планы тренировок (название, описание, тренировки) текущего пользователя.
    """
    try:
        logger.info(f"Fetching training plans for current user {current_user.id}")
        
        statement = (
            select(models.TrainingPlan)
            .join(models.TrainingPlanUser, models.TrainingPlan.id == models.TrainingPlanUser.план_тренировки_id)
            .where(models.TrainingPlanUser.пользователь_id == current_user.id)
            .options(
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.exercise_type),
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.difficulty_level),
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.equipment)
            )
            .distinct()
        )
        
        plans = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(plans)} training plans for current user")
        return plans
    except Exception as e:
        logger.error(f"Error fetching training plans for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/training-plans", response_model=schemas.TrainingPlan)
def create_training_plan(
    plan: schemas.TrainingPlanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting training plan creation with data: {plan.model_dump()}")
        
        # Create the training plan
        plan_data = plan.model_dump(exclude={'workouts'})
        db_plan = models.TrainingPlan(**plan_data)
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        
        # Add workouts to the plan
        if plan.workouts:
            for workout_id in plan.workouts:
                workout = db.get(models.Workout, workout_id)
                if not workout:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Workout with ID {workout_id} not found"
                    )
                db_plan.workouts.append(workout)
            
            db.add(db_plan)
            db.commit()
            db.refresh(db_plan)
        
        # Link the plan to the current user
        plan_user = models.TrainingPlanUser(
            план_тренировки_id=db_plan.id,
            пользователь_id=current_user.id
        )
        db.add(plan_user)
        db.commit()
        
        # Fetch the complete plan with all related data
        statement = (
            select(models.TrainingPlan)
            .where(models.TrainingPlan.id == db_plan.id)
            .options(
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.exercise_type),
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.difficulty_level),
                selectinload(models.TrainingPlan.workouts).selectinload(models.Workout.exercises).selectinload(models.Exercise.equipment)
            )
        )
        complete_plan = db.exec(statement).first()
        
        logger.info(f"Successfully created training plan with ID: {db_plan.id}")
        return complete_plan
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating training plan: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/training-plans/{plan_id}", response_model=schemas.MessageResponse)
def delete_training_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting training plan deletion for ID: {plan_id}")
        
        # Получаем план тренировок
        db_plan = db.get(models.TrainingPlan, plan_id)
        if not db_plan:
            logger.warning(f"Training plan not found with ID: {plan_id}")
            raise HTTPException(status_code=404, detail="Training plan not found")
        
        # Проверяем, принадлежит ли план текущему пользователю
        plan_user = db.exec(
            select(models.TrainingPlanUser)
            .where(models.TrainingPlanUser.план_тренировки_id == plan_id)
            .where(models.TrainingPlanUser.пользователь_id == current_user.id)
        ).first()
        
        if not plan_user:
            raise HTTPException(status_code=403, detail="Not authorized to delete this training plan")
        
        # Удаляем связь с пользователем
        db.delete(plan_user)
        
        # Очищаем связи с тренировками
        db_plan.workouts = []
        
        # Удаляем сам план
        db.delete(db_plan)
        db.commit()
        
        logger.info(f"Successfully deleted training plan with ID: {plan_id}")
        return {"message": "Training plan deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting training plan: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ===== Workouts CRUD =====
@app.get("/my-workouts", response_model=List[schemas.Workout])
def get_all_workouts_by_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить все тренировки (название, формат, время начала, упражнения) текущего пользователя.
    """
    try:
        logger.info(f"Fetching workouts for current user {current_user.id}")
        
        statement = (
            select(models.Workout)
            .join(models.WorkoutUser, models.Workout.id == models.WorkoutUser.тренировка_id)
            .where(models.WorkoutUser.пользователь_id == current_user.id)
            .options(
                selectinload(models.Workout.workout_exercises).selectinload(models.WorkoutExercise.exercise).selectinload(models.Exercise.exercise_type),
                selectinload(models.Workout.workout_exercises).selectinload(models.WorkoutExercise.exercise).selectinload(models.Exercise.difficulty_level),
                selectinload(models.Workout.workout_exercises).selectinload(models.WorkoutExercise.exercise).selectinload(models.Exercise.equipment)
            )
            .distinct()
        )
        
        workouts = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(workouts)} workouts for current user")
        return workouts
    except Exception as e:
        logger.error(f"Error fetching workouts for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workouts", response_model=schemas.Workout)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting workout creation with data: {workout.model_dump()}")
        # Create workout without exercises first
        workout_data = workout.model_dump(exclude={'exercises'})

        db_workout = models.Workout(**workout_data)
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        
        # Add exercises to the workout
        for exercise_data in workout.exercises:
            # Verify exercise stage exists
            exercise_stage = db.get(models.ExerciseStage, exercise_data.этап_упражнения_id)
            if not exercise_stage:
                raise HTTPException(
                    status_code=404,
                    detail=f"Exercise stage with ID {exercise_data.этап_упражнения_id} not found"
                )
                
            workout_exercise = models.WorkoutExercise(
                тренировка_id=db_workout.id,
                **exercise_data.model_dump()
            )
            db.add(workout_exercise)
        
        # Связываем тренировку с пользователем
        workout_user = models.WorkoutUser(
            тренировка_id=db_workout.id,
            пользователь_id=current_user.id
        )
        db.add(workout_user)
        db.commit()
        
        # Refresh the workout to include exercises
        db.refresh(db_workout)
        
        logger.info(f"Successfully created workout with ID: {db_workout.id}")
        return db_workout
    except Exception as e:
        logger.error(f"Error creating workout: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/workouts/{workout_id}", response_model=schemas.MessageResponse)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting workout deletion for ID: {workout_id}")
        db_workout = db.get(models.Workout, workout_id)
        if not db_workout:
            logger.warning(f"Workout not found with ID: {workout_id}")
            raise HTTPException(status_code=404, detail="Workout not found")
            
        # Проверяем, принадлежит ли тренировка текущему пользователю
        workout_user = db.exec(
            select(models.WorkoutUser)
            .where(models.WorkoutUser.тренировка_id == workout_id)
            .where(models.WorkoutUser.пользователь_id == current_user.id)
        ).first()
        
        if not workout_user:
            raise HTTPException(status_code=403, detail="Not authorized to delete this workout")
        
        # Удаляем все связанные упражнения тренировки
        workout_exercises = db.exec(
            select(models.WorkoutExercise)
            .where(models.WorkoutExercise.тренировка_id == workout_id)
        ).all()
        
        for exercise in workout_exercises:
            db.delete(exercise)
        
        # Удаляем связь с пользователем
        db.delete(workout_user)
        
        # Удаляем тренировку
        db.delete(db_workout)
        db.commit()
        
        logger.info(f"Successfully deleted workout with ID: {workout_id}")
        return {"message": "Workout deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting workout: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ===== Exercises CRUD =====
@app.get("/my-exercises", response_model=List[schemas.Exercise])
def get_all_exercises_by_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить все упражнения (название, тип, уровень сложности, описание, оборудование) 
    из тренировок текущего пользователя.
    """
    try:
        logger.info(f"Fetching exercises for current user {current_user.id}")
        
        statement = (
            select(models.Exercise)
            .join(models.ExerciseUser, models.Exercise.id == models.ExerciseUser.упражнение_id)
            .where(models.ExerciseUser.пользователь_id == current_user.id)
            .options(
                selectinload(models.Exercise.exercise_type),
                selectinload(models.Exercise.difficulty_level),
                selectinload(models.Exercise.equipment)
            )
            .distinct()
        )
        
        exercises = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(exercises)} exercises for current user")
        return exercises
    except Exception as e:
        logger.error(f"Error fetching exercises for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/exercises", response_model=schemas.Exercise)
def create_exercise(
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting exercise creation with data: {exercise.model_dump()}")
        db_exercise = models.Exercise(**exercise.model_dump())
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)

        # Связываем упражнение с пользователем
        exercise_user = models.ExerciseUser(
            упражнение_id=db_exercise.id,
            пользователь_id=current_user.id
        )
        db.add(exercise_user)
        db.commit()
        db.refresh(db_exercise)

        logger.info(f"Successfully created exercise with ID: {db_exercise.id}")
        return db_exercise
    except Exception as e:
        logger.error(f"Error creating exercise: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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
@app.get("/my-steps-by-dates", response_model=List[schemas.Steps])
def get_my_steps_by_dates(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить записи о шагах (количество шагов, цель, дата записи) текущего пользователя за период.
    Период задается датой начала и датой конца (включительно).
    """
    try:
        logger.info(f"Fetching steps for current user {current_user.id} from {start_date} to {end_date}")
        
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date cannot be later than end date"
            )
            
        statement = (
            select(models.Steps)
            .where(models.Steps.пользователь_id == current_user.id)
            .where(models.Steps.дата >= start_date)
            .where(models.Steps.дата <= end_date)
            .order_by(models.Steps.дата)
        )
        
        steps = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(steps)} steps records for current user")
        return steps
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching steps for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/steps", response_model=schemas.Steps)
def create_steps(
    steps: schemas.StepsCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting steps record creation with data: {steps.model_dump()}")
        steps_data = steps.model_dump()
        steps_data["пользователь_id"] = current_user.id
        db_steps = models.Steps(**steps_data)
        db.add(db_steps)
        db.commit()
        db.refresh(db_steps)
        logger.info(f"Successfully created steps record with ID: {db_steps.id}")
        return db_steps
    except Exception as e:
        logger.error(f"Error creating steps record: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/steps/{steps_id}", response_model=schemas.MessageResponse)
def delete_steps(
    steps_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    logger.info(f"Starting steps record deletion for ID: {steps_id}")
    db_steps = db.get(models.Steps, steps_id)
    if not db_steps:
        logger.warning(f"Steps record not found with ID: {steps_id}")
        raise HTTPException(status_code=404, detail="Steps record not found")
    # Check if the steps record belongs to the current user
    if db_steps.пользователь_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this steps record")
    
    db.delete(db_steps)
    db.commit()
    logger.info(f"Successfully deleted steps record with ID: {steps_id}")
    return {"message": "Steps record deleted successfully"}

@app.get("/my-waters-by-dates", response_model=List[schemas.Water])
def get_my_water_by_dates(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить записи о потреблении воды (количество воды, цель, дата) текущего пользователя за период.
    Период задается датой начала и датой конца (включительно).
    """
    try:
        logger.info(f"Fetching water records for current user {current_user.id} from {start_date} to {end_date}")
        
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date cannot be later than end date"
            )
            
        statement = (
            select(models.Water)
            .where(models.Water.пользователь_id == current_user.id)
            .where(models.Water.дата >= start_date)
            .where(models.Water.дата <= end_date)
            .order_by(models.Water.дата)
        )
        
        water_records = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(water_records)} water records for current user")
        return water_records
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching water records for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/water", response_model=schemas.Water)
def create_water(
    water: schemas.WaterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting water record creation with data: {water.model_dump()}")
        db_water = models.Water(**water.model_dump(), пользователь_id=current_user.id)
        db.add(db_water)
        db.commit()
        db.refresh(db_water)
        logger.info(f"Successfully created water record with ID: {db_water.id}")
        return db_water
    except Exception as e:
        logger.error(f"Error creating water record: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/water/{water_id}", response_model=schemas.MessageResponse)
def delete_water(
    water_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    logger.info(f"Starting water record deletion for ID: {water_id}")
    db_water = db.get(models.Water, water_id)
    if not db_water:
        logger.warning(f"Water record not found with ID: {water_id}")
        raise HTTPException(status_code=404, detail="Water record not found")
    # Check if the water record belongs to the current user
    if db_water.пользователь_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this water record")
    
    db.delete(db_water)
    db.commit()
    logger.info(f"Successfully deleted water record with ID: {water_id}")
    return {"message": "Water record deleted successfully"}

# ===== Diaries CRUD =====
@app.get("/my-diaries-by-dates", response_model=List[schemas.Diary])
def get_my_diaries_by_dates(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Получить дневниковые записи (дата записи, текстовая заметка, файл) текущего пользователя за период.
    Период задается датой начала и датой конца (включительно).
    """
    try:
        logger.info(f"Fetching diary entries for current user {current_user.id} from {start_date} to {end_date}")
        
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date cannot be later than end date"
            )
            
        statement = (
            select(models.Diary)
            .where(models.Diary.пользователь_id == current_user.id)
            .where(models.Diary.дата >= start_date)
            .where(models.Diary.дата <= end_date)
            .order_by(models.Diary.дата)
        )
        
        diaries = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(diaries)} diary entries for current user")
        return diaries
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching diary entries for current user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diaries", response_model=schemas.Diary)
def create_diary(
    diary: schemas.DiaryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting diary creation for user {current_user.id}")
        diary_data = diary.model_dump(exclude={'feelings', 'feeling_reasons'})
        diary_data["пользователь_id"] = current_user.id
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


@app.delete("/diaries/{diary_id}", response_model=schemas.MessageResponse)
def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        logger.info(f"Starting diary deletion for ID: {diary_id}")
        db_diary = db.get(models.Diary, diary_id)
        if not db_diary:
            logger.warning(f"Diary not found with ID: {diary_id}")
            raise HTTPException(status_code=404, detail="Diary not found")
        # Check if the diary belongs to the current user
        if db_diary.пользователь_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this diary")
            
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

# ===== Exercise Types and Difficulty Levels =====
@app.get("/exercise-types", response_model=List[schemas.ExerciseType])
def get_exercise_types(db: Session = Depends(get_db)):
    """
    Получить список всех типов упражнений.
    """
    try:
        logger.info("Fetching exercise types")
        statement = select(models.ExerciseType)
        types = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(types)} exercise types")
        return types
    except Exception as e:
        logger.error(f"Error fetching exercise types: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercise-difficulty-levels", response_model=List[schemas.ExerciseDifficulty])
def get_exercise_difficulty_levels(db: Session = Depends(get_db)):
    """
    Получить список всех уровней сложности упражнений.
    """
    try:
        logger.info("Fetching exercise difficulty levels")
        statement = select(models.ExerciseDifficulty)
        levels = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(levels)} difficulty levels")
        return levels
    except Exception as e:
        logger.error(f"Error fetching exercise difficulty levels: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercise-stages", response_model=List[schemas.ExerciseStage])
def get_exercise_stages(db: Session = Depends(get_db)):
    """
    Получить список всех этапов упражнений.
    """
    try:
        logger.info("Fetching exercise stages")
        statement = select(models.ExerciseStage)
        stages = db.exec(statement).all()
        logger.info(f"Successfully retrieved {len(stages)} exercise stages")
        return stages
    except Exception as e:
        logger.error(f"Error fetching exercise stages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
