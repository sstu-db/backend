from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

# Base models (no dependencies)
class User(SQLModel, table=True):
    __tablename__ = 'пользователь'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    дата_рождения: date
    имя: str
    фамилия: str
    отчество: str
    
    # client: Optional["Client"] = Relationship(back_populates="user")
    # trainer: Optional["Trainer"] = Relationship(back_populates="user")
    # training_plans: List["TrainingPlan"] = Relationship(back_populates="users", link_model=TrainingPlanUser)
    # workouts: List["Workout"] = Relationship(back_populates="users", link_model=WorkoutUser)
    diaries: List["Diary"] = Relationship(back_populates="user")

# class TrainingGoal(SQLModel, table=True):
#     __tablename__ = 'цель_тренировок'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str

# class PreparationLevel(SQLModel, table=True):
#     __tablename__ = 'уровень_подготовки'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str

# class WorkoutType(SQLModel, table=True):
#     __tablename__ = 'вид_тренировки'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str

# class ExerciseType(SQLModel, table=True):
#     __tablename__ = 'тип_упражнения'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str

# class DifficultyLevel(SQLModel, table=True):
#     __tablename__ = 'уровень_сложности'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str

# Link models (association tables)
# class TrainerClient(SQLModel, table=True):
#     __tablename__ = 'тренер_и_клиент'
    
#     тренер_id: int = Field(foreign_key='тренер.id', primary_key=True)
#     клиент_id: int = Field(foreign_key='клиент.id', primary_key=True)

# class TrainerSpecialtyLink(SQLModel, table=True):
#     __tablename__ = 'тренер_и_специальность'
    
#     тренер_id: int = Field(foreign_key='тренер.id', primary_key=True)
#     специальность_id: int = Field(foreign_key='специальность_тренера.id', primary_key=True)

# class TrainingPlanUser(SQLModel, table=True):
#     __tablename__ = 'план_тренировок_и_пользователь'
    
#     план_тренировок_id: int = Field(foreign_key='план_тренировок.id', primary_key=True)
#     пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

# class WorkoutUser(SQLModel, table=True):
#     __tablename__ = 'тренировка_и_пользователь'
    
#     тренировка_id: int = Field(foreign_key='тренировка.id', primary_key=True)
#     пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

# class WorkoutExercise(SQLModel, table=True):
#     __tablename__ = 'тренировка_и_упражнение'
    
#     тренировка_id: int = Field(foreign_key='тренировка.id', primary_key=True)
#     упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)

# class ExerciseUser(SQLModel, table=True):
#     __tablename__ = 'упражнение_и_пользователь'
    
#     упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
#     пользователь_id: int = Field(foreign_key='пользователь.id', primary_key=True)

# class ExerciseMuscle(SQLModel, table=True):
#     __tablename__ = 'упражнение_и_мышца'
    
#     упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
#     мышца_id: int = Field(foreign_key='мышца.id', primary_key=True)
#     важность: int

# class ExerciseEquipment(SQLModel, table=True):
#     __tablename__ = 'упражнение_и_снаряжение'
    
#     упражнение_id: int = Field(foreign_key='упражнение.id', primary_key=True)
#     снаряжение_id: int = Field(foreign_key='снаряжение.id', primary_key=True)

class DiaryFeeling(SQLModel, table=True):
    __tablename__ = 'дневник_и_чувство'
    
    дневник_id: int = Field(foreign_key='дневник.id', primary_key=True)
    чувство_id: int = Field(foreign_key='чувство.id', primary_key=True)

class DiaryFeelingReason(SQLModel, table=True):
    __tablename__ = 'дневник_и_причина_чувства'
    
    дневник_id: int = Field(foreign_key='дневник.id', primary_key=True)
    причина_чувства_id: int = Field(foreign_key='причина_чувства.id', primary_key=True)

class FileType(SQLModel, table=True):
    __tablename__ = 'файл_и_тип_файла'
    
    файл_id: int = Field(foreign_key='файл.id', primary_key=True)
    тип_файла_id: int = Field(foreign_key='тип_файла.id', primary_key=True)

# Models with relationships
# class Muscle(SQLModel, table=True):
#     __tablename__ = 'мышца'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
    
#     exercises: List["Exercise"] = Relationship(back_populates="muscles", link_model=ExerciseMuscle)

# class Equipment(SQLModel, table=True):
#     __tablename__ = 'снаряжение'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
    
#     exercises: List["Exercise"] = Relationship(back_populates="equipment", link_model=ExerciseEquipment)

class Feeling(SQLModel, table=True):
    __tablename__ = 'чувство'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str
    
    diaries: List["Diary"] = Relationship(back_populates="feelings", link_model=DiaryFeeling)

class FeelingReason(SQLModel, table=True):
    __tablename__ = 'причина_чувства'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str
    
    diaries: List["Diary"] = Relationship(back_populates="feeling_reasons", link_model=DiaryFeelingReason)

class FileTypeModel(SQLModel, table=True):
    __tablename__ = 'тип_файла'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    название: str
    
    files: List["File"] = Relationship(back_populates="file_types", link_model=FileType)

# class Client(SQLModel, table=True):
#     __tablename__ = 'клиент'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     пользователь_id: int = Field(foreign_key='пользователь.id')
#     цель_тренировок_id: int = Field(foreign_key='цель_тренировок.id')
#     уровень_подготовки_id: int = Field(foreign_key='уровень_подготовки.id')
    
#     user: "User" = Relationship(back_populates="client")
#     training_goal: "TrainingGoal" = Relationship()
#     preparation_level: "PreparationLevel" = Relationship()
#     trainers: List["Trainer"] = Relationship(back_populates="clients", link_model=TrainerClient)

# class Trainer(SQLModel, table=True):
#     __tablename__ = 'тренер'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     пользователь_id: int = Field(foreign_key='пользователь.id')
    
#     user: "User" = Relationship(back_populates="trainer")
#     specialties: List["TrainerSpecialty"] = Relationship(back_populates="trainers", link_model=TrainerSpecialtyLink)
#     clients: List["Client"] = Relationship(back_populates="trainers", link_model=TrainerClient)

# class TrainerSpecialty(SQLModel, table=True):
#     __tablename__ = 'специальность_тренера'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
    
#     trainers: List["Trainer"] = Relationship(back_populates="specialties", link_model=TrainerSpecialtyLink)

# class TrainingPlan(SQLModel, table=True):
#     __tablename__ = 'план_тренировок'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
#     описание: str
    
#     workouts: List["Workout"] = Relationship(back_populates="training_plan")
#     users: List["User"] = Relationship(back_populates="training_plans", link_model=TrainingPlanUser)

# class Workout(SQLModel, table=True):
#     __tablename__ = 'тренировка'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
#     формат_проведения: str
#     время_начала: str
#     вид_тренировки_id: int = Field(foreign_key='вид_тренировки.id')
#     план_тренировок_id: int = Field(foreign_key='план_тренировок.id')
    
#     workout_type: "WorkoutType" = Relationship()
#     training_plan: "TrainingPlan" = Relationship(back_populates="workouts")
#     exercises: List["Exercise"] = Relationship(back_populates="workouts", link_model=WorkoutExercise)
#     users: List["User"] = Relationship(back_populates="workouts", link_model=WorkoutUser)

# class Exercise(SQLModel, table=True):
#     __tablename__ = 'упражнение'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     название: str
#     тип_упражнения_id: int = Field(foreign_key='тип_упражнения.id')
#     уровень_сложности_id: int = Field(foreign_key='уровень_сложности.id')
#     описание: str
    
#     exercise_type: "ExerciseType" = Relationship()
#     difficulty_level: "DifficultyLevel" = Relationship()
#     workouts: List["Workout"] = Relationship(back_populates="exercises", link_model=WorkoutExercise)
#     muscles: List["Muscle"] = Relationship(back_populates="exercises", link_model=ExerciseMuscle)
#     equipment: List["Equipment"] = Relationship(back_populates="exercises", link_model=ExerciseEquipment)
#     users: List["User"] = Relationship(back_populates="exercises", link_model=ExerciseUser)

# class Steps(SQLModel, table=True):
#     __tablename__ = 'шаги'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     количество_шагов: int
#     цель_шагов: int
#     дата: date
#     пользователь_id: int = Field(foreign_key='пользователь.id')
    
#     user: "User" = Relationship(back_populates="steps")

# class Water(SQLModel, table=True):
#     __tablename__ = 'вода'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     объем_выпитой_воды: int
#     цель: int
#     дата: date
#     пользователь_id: int = Field(foreign_key='пользователь.id')
    
#     user: "User" = Relationship(back_populates="water")

class File(SQLModel, table=True):
    __tablename__ = 'файл'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    имя_файла: str
    
    diaries: List["Diary"] = Relationship(back_populates="file")
    file_types: List["FileTypeModel"] = Relationship(back_populates="files", link_model=FileType)

class Diary(SQLModel, table=True):
    __tablename__ = 'дневник'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    пользователь_id: int = Field(foreign_key='пользователь.id')
    дата: date
    запись: str
    файл_id: Optional[int] = Field(default=None, foreign_key='файл.id')
    
    feelings: List["Feeling"] = Relationship(back_populates="diaries", link_model=DiaryFeeling)
    feeling_reasons: List["FeelingReason"] = Relationship(back_populates="diaries", link_model=DiaryFeelingReason)
    file: Optional["File"] = Relationship(back_populates="diaries")
    user: "User" = Relationship(back_populates="diaries")