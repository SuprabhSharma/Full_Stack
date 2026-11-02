import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

## Get url from .env file
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)


## Create engine = the road to the database
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print(f"Connected to {version.split(',')[0]}")


# DeclarativeBase is the Parent class from SQLAlchemy that turn normal python class into a database table

# Declartive : You declare(describe) what a table look like
# Base : Its the Parent class everything else built on top of this
# like in pydantic we have BaseModel similarly we have DeclarativeBase for creating tables 


class Base(DeclarativeBase):
    pass


class StudentDB(Base):
    __tablename__ = "students_records"
    id = Column(String, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(50), nullable=False)
    marks = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Bind every session travels to this road
# metadata means all the table that inherits Base Class
# create_all() method to create the tables
Base.metadata.create_all(bind=engine)
print("Table ready ....")

# Step-4 (Creating a session means One visit , open , do work , close )

SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

if db.get(StudentDB, "S001") is None:
    db.add(
        StudentDB(
            id="S001",
            name="Aarav Sharma",
            age=25,
            course="Python",
            marks=80,
            email="aarav@example.com",
        )
    )
    db.commit()

# To Read it back

for i in db.query(StudentDB).all():
    print(i.id , i.name ,i.age , i.course, i.marks , i.email)
    
    
# Update 
aarav = db.get(StudentDB , "S001")
aarav.marks = 90
db.commit()