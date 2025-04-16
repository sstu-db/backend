from sqlmodel import SQLModel, create_engine, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/app"

# Create SQLModel engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session 