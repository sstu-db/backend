from pydantic import BaseModel, EmailStr
from typing import List, Optional, ForwardRef
from datetime import date, datetime

# ===== Forward References =====
UserRef = ForwardRef('User')
ClientRef = ForwardRef('Client')
TrainerRef = ForwardRef('Trainer')

# ===== Authentication Schemas =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ===== Registration Schemas =====

class RegisterBase(BaseModel):
    почта: EmailStr
    хэш_пароля: str
    дата_рождения: Optional[date] = None
    имя: str
    фамилия: str
    отчество: Optional[str] = None

class ClientRegister(RegisterBase):
    уровень_подготовки_id: Optional[int] = None
    training_goals: Optional[List[int]] = None  # List of training goal IDs
    training_types: Optional[List[int]] = None  # List of training type IDs

class TrainerRegister(RegisterBase):
    specialties: Optional[List[int]] = None  # List of specialty IDs

# ===== Base User Schemas =====
class UserBase(BaseModel):
    дата_рождения: Optional[date] = None
    имя: str
    фамилия: str
    отчество: Optional[str] = None

class ClientBase(BaseModel):
    уровень_подготовки_id: Optional[int] = None
    пользователь_id: int

class TrainerBase(BaseModel):
    пользователь_id: int

# ===== Base Content Schemas =====
class ExerciseBase(BaseModel):
    название: str
    описание: Optional[str] = None
    тип_упражнения_id: int
    сложность_упражнения_id: int

class WorkoutBase(BaseModel):
    название: str
    является_онлайн: bool
    время_начала: datetime

class TrainingPlanBase(BaseModel):
    название: str
    описание: Optional[str] = None

class DiaryBase(BaseModel):
    дата: date
    запись: str
    файл_id: Optional[int] = None

class StepsBase(BaseModel):
    колво: int
    целевое_колво: int
    дата: date

class WaterBase(BaseModel):
    объем: float
    целевой_объем: float
    дата: date

# ===== Reference Data Schemas =====
class PreparationLevel(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class TrainerSpecialty(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class TrainingGoal(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class TrainingType(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class ExerciseType(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class ExerciseDifficulty(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class Equipment(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class FileType(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class Feeling(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class FeelingReason(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

class ExerciseStage(BaseModel):
    id: int
    название: str

    class Config:
        from_attributes = True

# ===== User Response Schemas =====
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Client(ClientBase):
    id: int
    user: Optional[UserRef] = None
    preparation_level: Optional[PreparationLevel] = None
    training_goals: List[TrainingGoal] = []
    training_types: List[TrainingType] = []

    class Config:
        from_attributes = True

class Trainer(TrainerBase):
    id: int
    user: Optional[UserRef] = None
    specialties: List[TrainerSpecialty] = []

    class Config:
        from_attributes = True

# ===== Content Response Schemas =====
class File(BaseModel):
    id: int
    имя_файла: str
    file_types: List[FileType] = []

    class Config:
        from_attributes = True

class Exercise(ExerciseBase):
    id: int
    exercise_type: Optional[ExerciseType] = None
    difficulty_level: Optional[ExerciseDifficulty] = None
    equipment: List[Equipment] = []
    exercise_stage: Optional[ExerciseStage] = None

    class Config:
        from_attributes = True

class WorkoutExerciseCreate(BaseModel):
    упражнение_id: int
    этап_упражнения_id: int
    номер_в_очереди: int
    колво_подходов: int
    колво_подходов_выполнено: int
    колво_повторений: int
    колво_повторений_выполнено: int

    class Config:
        from_attributes = True

class WorkoutExercise(WorkoutExerciseCreate):
    exercise: Optional[Exercise] = None

    class Config:
        from_attributes = True

class Workout(WorkoutBase):
    id: int
    workout_exercises: List[WorkoutExercise]

    class Config:
        from_attributes = True

class TrainingPlan(TrainingPlanBase):
    id: int
    workouts: List[Workout] = []

    class Config:
        from_attributes = True

class Diary(DiaryBase):
    id: int
    пользователь_id: int
    feelings: List[Feeling] = []
    feeling_reasons: List[FeelingReason] = []
    file: Optional[File] = None

    class Config:
        from_attributes = True

class Steps(StepsBase):
    id: int

    class Config:
        from_attributes = True

class Water(WaterBase):
    id: int

    class Config:
        from_attributes = True

# ===== Request Schemas =====
class ClientTrainersRequest(BaseModel):
    клиент_id: int

class TrainerClientsRequest(BaseModel):
    тренер_id: int

class TrainingPlanRequest(BaseModel):
    клиент_id: Optional[int] = None
    тренер_id: Optional[int] = None

class WorkoutsRequest(BaseModel):
    клиент_id: Optional[int] = None
    тренер_id: Optional[int] = None

class ExercisesRequest(BaseModel):
    клиент_id: Optional[int] = None
    тренер_id: Optional[int] = None

class DiaryRequest(BaseModel):
    пользователь_id: int
    дата: Optional[date] = None
    дата_начала: Optional[date] = None
    дата_конца: Optional[date] = None

class StepsRequest(BaseModel):
    пользователь_id: int
    дата: Optional[date] = None
    дата_начала: Optional[date] = None
    дата_конца: Optional[date] = None

class WaterRequest(BaseModel):
    пользователь_id: int
    дата: Optional[date] = None
    дата_начала: Optional[date] = None
    дата_конца: Optional[date] = None

# ===== Response Schemas =====
class ClientTrainersResponse(BaseModel):
    data: List[Trainer]

    class Config:
        from_attributes = True

class TrainerClientsResponse(BaseModel):
    data: List[Client]

    class Config:
        from_attributes = True

class TrainingPlanResponse(BaseModel):
    data: List[TrainingPlan]

class WorkoutsResponse(BaseModel):
    data: List[Workout]

class ExercisesResponse(BaseModel):
    data: List[Exercise]

class DiaryResponse(BaseModel):
    data: List[Diary]

class StepsResponse(BaseModel):
    data: List[Steps]

class WaterResponse(BaseModel):
    data: List[Water]

# ===== Create Schemas =====
class ExerciseCreate(ExerciseBase):
    pass

    class Config:
        from_attributes = True

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate]

    class Config:
        from_attributes = True

class TrainingPlanCreate(TrainingPlanBase):
    workouts: List[int] = []  # List of workout IDs to include in the plan

    class Config:
        from_attributes = True

class DiaryCreate(DiaryBase):
    feelings: Optional[List[int]] = None  # List of feeling IDs
    feeling_reasons: Optional[List[int]] = None  # List of feeling reason IDs

    class Config:
        from_attributes = True

class StepsCreate(StepsBase):
    class Config:
        from_attributes = True

class WaterCreate(WaterBase):
    class Config:
        from_attributes = True

# ===== Utility Schemas =====
class MessageResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str

# Update forward references
User.model_rebuild()
Client.model_rebuild()
Trainer.model_rebuild() 