import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_validator,
)
from sqlalchemy import Column, Integer, String, create_engine, func, text
from sqlalchemy.exc import IntegrityError  ## exception
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# Part 1 : Load Database url from the .env file

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Part 2 Create the engine ( connection to the Database PostgreSQL)

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print(f"Connected to {version.split(',')[0]}")


# Part 3 Create SessionLocal and Base

SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()  # Creates a new sqlalchemy session


class Base(DeclarativeBase):
    pass


## Part -4 Create Student_DB Table and Bind it


class StudentDB(Base):
    __tablename__ = "students_records"
    id = Column(String, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(50), nullable=False)
    marks = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)


Base.metadata.create_all(bind=engine)
print("Table ready ....")


# Part -5 Pydantic Schemas for input (StudentCreate , StudentUpdate)


class StudentCreate(BaseModel):
    id: str = Field(..., examples=["S001"])
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, le=100)
    email: EmailStr
    course: str = Field(..., min_length=2, max_length=50)
    marks: int = Field(..., ge=0, le=100)

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Value must contain only letters and spaces")

        return value.title()


class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    age: int | None = Field(None, gt=0, le=100)
    email: EmailStr | None = None
    course: str | None = Field(None, min_length=2, max_length=50)
    marks: int | None = Field(None, ge=0, le=100)

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain Letters and spaces only ")

        return value.title()


# Part 6: Pydantic Schemas for the output to add addtional reponse from server
# From_attributes True lest pydantic to read student.marks (an object) not only student["marks"]
class StudentResponse(StudentCreate):
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        else:
            return "C"


# Part-7 get_db() - one session per request

# Opens a session, pauses at yield while the endpoint while the endpoint does its work and once the
# endpoint is completed its work the session will be close


def get_db():
    db = SessionLocal()
    try:
        yield db  # Holds the session untile it completes or raise http exception

    finally:
        db.close()  # cleans up the session and releases resources


# Part-8 : Create the FastAPI app
"""
Already Created Above

"""

### Depends(get_db) means before running this endpoint run get_db function and give me what that function is returning


# db.get is the orm operations to fetch the data from the database
# Part - 9 GET ONE  STUDENT
# Depends Before executing get_student() call get_db() and inject the database session it provides in the parameter db
@app.get("/student/{student_id}", response_model=StudentResponse , tags=["GET ROUTE"])
def get_student(
    student_id: str = Path(..., examples=["S001"]),
    db: Session = Depends(get_db),  # db recieves the session as database session object
):
    student = db.get(
        StudentDB, student_id
    )  # its similar to select ... where id = student_id where student contains that
    # get student_id from studentDB
    if student is None:
        raise HTTPException(
            status_code=404, detail=f"Student with id : {student_id} not found"
        )

    return student


## Post : Create a Student
@app.post("/student", response_model=StudentResponse, status_code=201 , tags=["POST ROUTE"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.get(StudentDB, student.id):
        raise HTTPException(
            status_code=404, detail=f"Student with id '{student.id}' already exists"
        )
    new_student = StudentDB(**student.model_dump())

    db.add(new_student)  ### here adds to the local session only not in database
    try:
        db.commit()  ### reflects in database
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email for student f'{student.email}' is already registered",
        )

    db.refresh(new_student)

    return new_student


### Update a Student
@app.put("/update_student/{student_id}" ,tags=["PUT ROUTE"])
def update_student(
    student_update: StudentUpdate,
    student_id: str = Path(
        ..., description="ID of the student that you want to delete"
    ),
    db: Session = Depends(get_db),
):
    student = db.get(StudentDB, student_id)

    if student is None:
        raise HTTPException(
            status_code=404, detail=f"Student with id '{student_id}' not found"
        )

    changes = student_update.model_dump(exclude_unset=True)

    for key, values in changes.items():
        setattr(student, key, values)

    try:
        db.commit()  ### reflects in database
    except IntegrityError:
        db.rollback()   ### undo the changes 
        raise HTTPException(
            status_code=400,
            detail="Email for student f'{student.email}' is already registered",
        )

    db.refresh(student)

    return student


@app.delete("/student/{student_id}" , tags=["DELETE ROUTE"])
def delete_student(
    student_id: str = Path(
        ..., description="The Id of the Student that you want to delete"
    ),
    db: Session = Depends(get_db),
):

    student = db.get(StudentDB, student_id)

    if student is None:
        raise HTTPException(
            status_code=404, detail=f"Student with id '{student_id}' not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student Deleted with ID {student_id} is deleted Sucessfully"}


# Part 13 Get all students ( filter , sort , paginate )

SORT_FIELDS = ["marks", "age", "name"]
SORT_ORDER = ["asc", "desc"]


@app.get("/students" ,tags=["GET ROUTE"])
def get_all(
    course : str | None= Query(None, description="show only students in this course", examples=["Python"]),
    sort_by : str | None = Query(None, description="Sort by marks, age or name"),
    order : str = Query("asc", description="asc or desc", examples=["desc"]),
    page : int = Query(1, ge=1, description="Which page you want (start from 1)"),
    limit:int = Query(2, ge=1, le=100 , description= "How many students on one page (1 to 100)"),
    db : Session = Depends(get_db)
):
    if sort_by is not None and sort_by not in SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by '{sort_by}', Choose from {SORT_FIELDS}")

    if order not in SORT_ORDER:
        raise HTTPException(status_code=400, detail=f"Invalid order '{order}', Choose from {SORT_ORDER}") 

    query = db.query(StudentDB) # Select * from student_records
    
    if course:                      # select * from student_records where course == "Python"
        query = query.filter(func.lower(StudentDB.course) == course.lower())
        
    total_students = query.count()
    
    if sort_by:
        column = getattr(StudentDB, sort_by )
        
        if order == 'desc':
            query = query.order_by(column.desc())   ## "marks" -> StudentDB.marks
            
        else:
            query = query.order_by(column.asc())
            
    else : 
        query = query.order_by(StudentDB.id)   # Fixed Order , so pages  never repeat student
            
     
    start = (page-1) * limit #page=2,limit=2 -> start = 2
    students = query.offset(start).limit(limit).all()

    return {
        "page" : page,
        "limit" : limit,
        "total_students": total_students,
        "students" : [StudentResponse.model_validate(student) for student in students]
    }
    
    
    
    