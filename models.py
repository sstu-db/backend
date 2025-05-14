from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator, constr, conint

# Link models (association tables)
class WorkoutUser(SQLModel, table=True):
    __tablename__ = 'тренировка_и_пользователь'
    
    тренировка_id: int = Field(foreign_key='тренировка.id', primary_key=True)
    пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

class TrainingPlanUser(SQLModel, table=True):
    __tablename__ = 'план_тренировки_и_пользователь'
    
    план_тренировки_id: int = Field(foreign_key='план_тренировки.id', primary_key=True)
    пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

class ExerciseUser(SQLModel, table=True):
    __tablename__ = 'упражнение_и_пользователь'
    
    упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
    пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

class DiaryFeeling(SQLModel, table=True):
    __tablename__ = 'дневник_и_чувство'
    
    дневник_id: int = Field(foreign_key='дневник.id', primary_key=True)
    чувство_id: int = Field(foreign_key='чувство.id', primary_key=True)

class DiaryFeelingReason(SQLModel, table=True):
    __tablename__ = 'дневник_и_причина_чувства'
    
    дневник_id: int = Field(foreign_key='дневник.id', primary_key=True)
    причина_чувства_id: int = Field(foreign_key='причина_чувства.id', primary_key=True)

class ClientTrainingGoal(SQLModel, table=True):
    __tablename__ = 'клиент_и_цель_тренировок'
    
    клиент_id: int = Field(foreign_key='клиент.id', primary_key=True)
    цель_тренировок_id: int = Field(foreign_key='цель_тренировок.id', primary_key=True)

class TrainerClient(SQLModel, table=True):
    __tablename__ = 'тренер_и_клиент'
    
    тренер_id: int = Field(foreign_key='тренер.id', primary_key=True)
    клиент_id: int = Field(foreign_key='клиент.id', primary_key=True)

class TrainerSpecialtyLink(SQLModel, table=True):
    __tablename__ = 'тренер_и_специальность'
    
    тренер_id: int = Field(foreign_key='тренер.id', primary_key=True)
    специальность_тренера_id: int = Field(foreign_key='специальность_тренера.id', primary_key=True)

class WorkoutTrainingPlan(SQLModel, table=True):
    __tablename__ = 'тренировка_и_план_тренировки'
    
    тренировка_id: int = Field(foreign_key='тренировка.id', primary_key=True)
    план_тренировки_id: int = Field(foreign_key='план_тренировки.id', primary_key=True)

class WorkoutExercise(SQLModel, table=True):
    __tablename__ = 'тренировка_и_упражнение'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    тренировка_id: int = Field(foreign_key='тренировка.id')
    упражнение_id: int = Field(foreign_key='упражнение.id')
    этап_упражнения_id: int = Field(foreign_key='этап_упражнения.id')
    номер_в_очереди: int = Field(ge=0)
    колво_подходов: int = Field(ge=1)
    колво_подходов_выполнено: int = Field(ge=1)
    колво_повторений: int = Field(ge=1)
    колво_повторений_выполнено: int = Field(ge=1)
    
    workout: "Workout" = Relationship(back_populates="workout_exercises")
    exercise: "Exercise" = Relationship(back_populates="workout_exercises")
    exercise_stage: "ExerciseStage" = Relationship(back_populates="workout_exercises")

class ExerciseEquipment(SQLModel, table=True):
    __tablename__ = 'упражнение_и_снаряжение'
    
    упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
    снаряжение_id: int = Field(foreign_key='снаряжение.id', primary_key=True)

class ExerciseFile(SQLModel, table=True):
    __tablename__ = 'упражнение_и_файл'
    
    упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
    файл_id: int = Field(foreign_key='файл.id', primary_key=True)

class FileFileType(SQLModel, table=True):
    __tablename__ = 'файл_и_тип_файла'
    
    файл_id: int = Field(foreign_key='файл.id', primary_key=True)
    тип_файла_id: int = Field(foreign_key='тип_файла.id', primary_key=True)

class ClientTrainingType(SQLModel, table=True):
    __tablename__ = 'клиент_и_тип_тренировки'
    
    клиент_id: int = Field(foreign_key='клиент.id', primary_key=True)
    тип_тренировки_id: int = Field(foreign_key='тип_тренировки.id', primary_key=True)

class UserAchievement(SQLModel, table=True):
    __tablename__ = 'пользователь_и_достижение'
    
    пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)
    достижение_id: int = Field(foreign_key='достижение.id', primary_key=True)

class ChatUser(SQLModel, table=True):
    __tablename__ = 'чат_и_пользователь'
    
    пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)
    чат_id: int = Field(foreign_key='чат.id', primary_key=True)

class MessageFile(SQLModel, table=True):
    __tablename__ = 'сообщение_и_файл'
    
    сообщение_id: int = Field(foreign_key='сообщение.id', primary_key=True)
    файл_id: int = Field(foreign_key='файл.id', primary_key=True)

# Base models (no dependencies)
class Gender(SQLModel, table=True):
    __tablename__ = 'пол'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    users: List["User"] = Relationship(back_populates="gender")

class User(SQLModel, table=True):
    __tablename__ = 'пользователь'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    дата_рождения: Optional[date] = None
    хэш_пароля: str = Field(max_length=255)
    почта: str = Field(max_length=255, unique=True)
    отчество: Optional[str] = Field(default=None, max_length=255)
    фамилия: Optional[str] = Field(default=None, max_length=255)
    имя: Optional[str] = Field(default=None, max_length=255)
    пол_id: Optional[int] = Field(default=None, foreign_key='пол.id')
    
    @field_validator('почта')
    @classmethod
    def validate_email(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Неверный формат email')
        return v
    
    @field_validator('отчество', 'фамилия', 'имя')
    @classmethod
    def validate_name(cls, v):
        if v is not None and not all(c.isalpha() for c in v):
            raise ValueError('Должно содержать только русские буквы')
        return v
    
    gender: Optional["Gender"] = Relationship(back_populates="users")
    client: Optional["Client"] = Relationship(back_populates="user")
    trainer: Optional["Trainer"] = Relationship(back_populates="user")
    training_plans: List["TrainingPlan"] = Relationship(back_populates="users", link_model=TrainingPlanUser)
    workouts: List["Workout"] = Relationship(back_populates="users", link_model=WorkoutUser)
    diaries: List["Diary"] = Relationship(back_populates="user")
    exercises: List["Exercise"] = Relationship(back_populates="users", link_model=ExerciseUser)
    steps: List["Steps"] = Relationship(back_populates="user")
    water: List["Water"] = Relationship(back_populates="user")

class PreparationLevel(SQLModel, table=True):
    __tablename__ = 'уровень_подготовки'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() for c in v):
            raise ValueError('Название должно содержать только русские буквы')
        return v
    
    clients: List["Client"] = Relationship(back_populates="preparation_level")

class TrainingGoal(SQLModel, table=True):
    __tablename__ = 'цель_тренировок'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    clients: List["Client"] = Relationship(back_populates="training_goals", link_model=ClientTrainingGoal)

class ExerciseType(SQLModel, table=True):
    __tablename__ = 'тип_упражнения'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    exercises: List["Exercise"] = Relationship(back_populates="exercise_type")

class ExerciseDifficulty(SQLModel, table=True):
    __tablename__ = 'сложность_упражнения'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    exercises: List["Exercise"] = Relationship(back_populates="difficulty_level")

class Equipment(SQLModel, table=True):
    __tablename__ = 'снаряжение'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    exercises: List["Exercise"] = Relationship(back_populates="equipment", link_model=ExerciseEquipment)

class Feeling(SQLModel, table=True):
    __tablename__ = 'чувство'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    diaries: List["Diary"] = Relationship(back_populates="feelings", link_model=DiaryFeeling)

class FeelingReason(SQLModel, table=True):
    __tablename__ = 'причина_чувства'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    diaries: List["Diary"] = Relationship(back_populates="feeling_reasons", link_model=DiaryFeelingReason)

class FileType(SQLModel, table=True):
    __tablename__ = 'тип_файла'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    files: List["File"] = Relationship(back_populates="file_types", link_model=FileFileType)

class TrainingType(SQLModel, table=True):
    __tablename__ = 'тип_тренировки'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    clients: List["Client"] = Relationship(back_populates="training_types", link_model=ClientTrainingType)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v

class TrainerSpecialty(SQLModel, table=True):
    __tablename__ = 'специальность_тренера'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    trainers: List["Trainer"] = Relationship(back_populates="specialties", link_model=TrainerSpecialtyLink)

class TrainingPlan(SQLModel, table=True):
    __tablename__ = 'план_тренировки'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255)
    описание: Optional[str] = None
    
    workouts: List["Workout"] = Relationship(back_populates="training_plan", link_model=WorkoutTrainingPlan)
    users: List["User"] = Relationship(back_populates="training_plans", link_model=TrainingPlanUser)

class Workout(SQLModel, table=True):
    __tablename__ = 'тренировка'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255)
    является_онлайн: Optional[bool] = None
    время_начала: Optional[datetime] = None
    
    training_plan: Optional["TrainingPlan"] = Relationship(back_populates="workouts", link_model=WorkoutTrainingPlan)
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="workout")
    users: List["User"] = Relationship(back_populates="workouts", link_model=WorkoutUser)
    exercises: List["Exercise"] = Relationship(
        back_populates="workouts",
        link_model=WorkoutExercise,
        sa_relationship_kwargs={"viewonly": True}
    )

class Exercise(SQLModel, table=True):
    __tablename__ = 'упражнение'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255)
    описание: Optional[str] = None
    тип_упражнения_id: int = Field(foreign_key='тип_упражнения.id')
    сложность_упражнения_id: int = Field(foreign_key='сложность_упражнения.id')
    
    exercise_type: "ExerciseType" = Relationship(back_populates="exercises")
    difficulty_level: "ExerciseDifficulty" = Relationship(back_populates="exercises")
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="exercise")
    equipment: List["Equipment"] = Relationship(back_populates="exercises", link_model=ExerciseEquipment)
    users: List["User"] = Relationship(back_populates="exercises", link_model=ExerciseUser)
    files: List["File"] = Relationship(back_populates="exercises", link_model=ExerciseFile)
    workouts: List["Workout"] = Relationship(
        back_populates="exercises",
        link_model=WorkoutExercise,
        sa_relationship_kwargs={"viewonly": True}
    )

class File(SQLModel, table=True):
    __tablename__ = 'файл'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    имя_файла: Optional[str] = Field(default=None, max_length=255)
    
    diaries: List["Diary"] = Relationship(back_populates="file")
    file_types: List["FileType"] = Relationship(back_populates="files", link_model=FileFileType)
    exercises: List["Exercise"] = Relationship(back_populates="files", link_model=ExerciseFile)

class Diary(SQLModel, table=True):
    __tablename__ = 'дневник'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    дата: date
    запись: str
    пользователь_id: int = Field(foreign_key='пользователь.id')
    файл_id: Optional[int] = Field(default=None, foreign_key='файл.id')
    
    feelings: List["Feeling"] = Relationship(back_populates="diaries", link_model=DiaryFeeling)
    feeling_reasons: List["FeelingReason"] = Relationship(back_populates="diaries", link_model=DiaryFeelingReason)
    file: Optional["File"] = Relationship(back_populates="diaries")
    user: "User" = Relationship(back_populates="diaries")

class Water(SQLModel, table=True):
    __tablename__ = 'вода'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    объем: int = Field(ge=0, le=10000)
    целевой_объем: Optional[int] = Field(default=None, ge=0, le=10000)
    дата: date
    пользователь_id: int = Field(foreign_key='пользователь.id')
    
    user: "User" = Relationship(back_populates="water")

class Steps(SQLModel, table=True):
    __tablename__ = 'шаги'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    колво: int = Field(ge=0)
    целевое_колво: Optional[int] = Field(default=None, ge=0)
    дата: date
    пользователь_id: int = Field(foreign_key='пользователь.id')
    
    user: "User" = Relationship(back_populates="steps")

class Client(SQLModel, table=True):
    __tablename__ = 'клиент'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    уровень_подготовки_id: Optional[int] = Field(default=None, foreign_key='уровень_подготовки.id')
    пользователь_id: int = Field(foreign_key='пользователь.id')
    
    user: "User" = Relationship(back_populates="client")
    preparation_level: Optional["PreparationLevel"] = Relationship(back_populates="clients")
    trainers: List["Trainer"] = Relationship(
        back_populates="clients",
        link_model=TrainerClient,
        sa_relationship_kwargs={
            "lazy": "select",
            "viewonly": True
        }
    )
    training_goals: List["TrainingGoal"] = Relationship(back_populates="clients", link_model=ClientTrainingGoal)
    training_types: List["TrainingType"] = Relationship(back_populates="clients", link_model=ClientTrainingType)

class Trainer(SQLModel, table=True):
    __tablename__ = 'тренер'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    пользователь_id: int = Field(foreign_key='пользователь.id', unique=True)
    
    user: "User" = Relationship(back_populates="trainer")
    specialties: List["TrainerSpecialty"] = Relationship(back_populates="trainers", link_model=TrainerSpecialtyLink)
    clients: List["Client"] = Relationship(
        back_populates="trainers",
        link_model=TrainerClient,
        sa_relationship_kwargs={
            "lazy": "select",
            "viewonly": True
        }
    )

class ExerciseStage(SQLModel, table=True):
    __tablename__ = 'этап_упражнения'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str = Field(max_length=255, unique=True)
    
    @field_validator('название')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Название должно содержать только русские буквы и пробелы')
        return v
    
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="exercise_stage")
