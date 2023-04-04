from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
import datetime
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
        title="Hello Birthday API",
        description="Revolut interview task"
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/hello/{username}", status_code=204)
def create_user(user_dob: schemas.UserDOB, username: str = Path(..., min_length=1), db: Session = Depends(get_db)):
    print(user_dob)
    if not username.isalpha():
        raise HTTPException(status_code=400, detail="Username must contain only letters.")
    if not user_dob.dateOfBirth:
        raise HTTPException(status_code=400, detail="Date of birth must be provided.")
    
    try:
        dob = datetime.datetime.strptime(user_dob.dateOfBirth, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD")
    if dob >= datetime.date.today():
        raise HTTPException(status_code=400, detail="Invalid date of birth.")
    crud.add_or_update_user(db, username, dob)


@app.get("/hello/{username}", response_model=schemas.Message)
def get_user(username: str = Path(..., min_length=1), db: Session = Depends(get_db)):
    if not username.isalpha():
        raise HTTPException(status_code=400, detail="Username must contain only letters")
    if not crud.user_exists_in_db(db, username):
         raise HTTPException(status_code=404, detail="User not found.")
    
    # Fetch the user's data from the database
    dob = crud.get_user_date_of_birth(db, username)
    if not dob:
        raise HTTPException(status_code=404, detail="User not found")
    
    today = datetime.date.today()
    if dob.month == today.month and dob.day == today.day:
        message = f"Hello, {username}! Happy birthday!"
    else:
        delta = (datetime.date(today.year+1, dob.month, dob.day) - today).days
        message = f"Hello, {username}! Your birthday is in {delta} day(s)"
    return JSONResponse(content={"message": message})

