from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

# Base schemas
class UserBase(BaseModel):
    дата_рождения: Optional[date] = None
    имя: str
    фамилия: str
    отчество: Optional[str] = None

class ClientBase(BaseModel):
    уровень_подготовки_id: int

class TrainerBase(BaseModel):
    id: int
    пользователь_id: int

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

# Response schemas for simple models
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

# Response schemas for complex models
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Client(ClientBase):
    id: int
    пользователь_id: int
    user: Optional[User] = None
    preparation_level: Optional[PreparationLevel] = None
    trainers: List["Trainer"] = []
    training_goals: List[TrainingGoal] = []

    class Config:
        from_attributes = True

class Trainer(TrainerBase):
    user: Optional[User] = None
    clients: List["Client"] = []
    specialties: List[TrainerSpecialty] = []

    class Config:
        from_attributes = True

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
    users: List[User] = []

    class Config:
        from_attributes = True

class Workout(WorkoutBase):
    id: int
    exercises: List[Exercise] = []
    users: List[User] = []

    class Config:
        from_attributes = True

class TrainingPlan(TrainingPlanBase):
    id: int
    workouts: List[Workout] = []
    users: List[User] = []

    class Config:
        from_attributes = True

class Diary(DiaryBase):
    id: int
    пользователь_id: int
    feelings: List[Feeling] = []
    feeling_reasons: List[FeelingReason] = []
    file: Optional[File] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True

class Steps(StepsBase):
    id: int
    пользователь_id: int
    user: Optional[User] = None

    class Config:
        from_attributes = True

class Water(WaterBase):
    id: int
    пользователь_id: int
    user: Optional[User] = None

    class Config:
        from_attributes = True

# Create schemas
class UserCreate(UserBase):
    pass

class ClientCreate(ClientBase):
    пользователь_id: int

    class Config:
        from_attributes = True

class TrainerCreate(TrainerBase):
    пользователь_id: int

    class Config:
        from_attributes = True

class ExerciseCreate(ExerciseBase):
    pass

    class Config:
        from_attributes = True

class WorkoutCreate(WorkoutBase):
    pass

    class Config:
        from_attributes = True

class TrainingPlanCreate(TrainingPlanBase):
    pass

    class Config:
        from_attributes = True

class DiaryCreate(DiaryBase):
    пользователь_id: int
    feelings: Optional[List[int]] = None  # List of feeling IDs
    feeling_reasons: Optional[List[int]] = None  # List of feeling reason IDs

    class Config:
        from_attributes = True

class StepsCreate(StepsBase):
    пользователь_id: int

    class Config:
        from_attributes = True

class WaterCreate(WaterBase):
    пользователь_id: int

    class Config:
        from_attributes = True

class TablesResponse(BaseModel):
    data: List[str]

class TableInfoResponse(BaseModel):
    table: str
    data: List[dict]

class QueryResponse(BaseModel):
    data: List[dict]

class TrainerResponse(TrainerBase):
    user: Optional[User] = None

    class Config:
        from_attributes = True

class ClientResponse(ClientBase):
    user: Optional[User] = None
    preparation_level: Optional[PreparationLevel] = None
    class Config:
        from_attributes = True

class TrainersResponse(BaseModel):
    data: List[TrainerResponse]

class ClientsResponse(BaseModel):
    data: List[ClientResponse]

class TrainingPlansResponse(BaseModel):
    data: List["TrainingPlan"]

class WorkoutsResponse(BaseModel):
    data: List["Workout"]

class ExercisesResponse(BaseModel):
    data: List["Exercise"]

class StepsResponse(BaseModel):
    data: List["Steps"]

class WaterResponse(BaseModel):
    data: List["Water"]

class DiariesResponse(BaseModel):
    data: List["Diary"]

class MessageResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str 