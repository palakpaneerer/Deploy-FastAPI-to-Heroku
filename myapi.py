# This code is how to deploy FastAPI to Heroku.
# I reffer tomitokko Github to make and understand this code.
# The below is the URL.
# https://github.com/tomitokko/fastapi-project/tree/main


# The function of Path：description,  verification rule such as gt & lt (greater than & less than).
from fastapi import FastAPI, Path
# By using Optional, we can use type hinting to ensure that variables are “optional.”
from typing import Optional
from pydantic import BaseModel



app = FastAPI()



# Assuming the data in the database.
students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    }
}



class Student(BaseModel):
    name: str
    age: int
    year: str

# "Optional[] = None" means not mandatory.
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None
    


# We can get {"name": "First Data"} on our screen when accessing this URL.
@app.get("/")
def index():
    return {"name": "First Data"}


# We can get students[student_id] information on our screen when accessing this URL.
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(
        None, # Thi is default. But this value will be from URL path above. 
        description="The ID of the student you want to view", # This is just explanation.
        gt=0, # greater than 0
        lt=3 # less than 3
        )):
    return students[student_id]


# We can get students[s_id] information on our screen when accessing this URL.
@app.get("/get-by-name/{student_id}")
def get_student(*,
                student_id: int,
                name: Optional[str] = None,
                test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}
    
# How to use * ?
# After *, we need to metion keyword to put the argument.
"""
def function(arg1, arg2, *, kwarg1, kwarg2):
    pass

function(1, 2, kwarg1=3, kwarg2=4)
"""    
    
    
# We can make a new student_id.
@app.post("/create-student/{student_id}")
def create_student(student_id : int,
                   student : Student): # Data type should be aligned with the Student class.
    if student_id in students:
        return {"Error": "Student exists"}

    students[student_id] = student
    return students[student_id]


# We can update the student information.
@app.put("/update-student/{student_id}")
def update_student(student_id: int,
                   student: UpdateStudent): # Data type should be aligned with the UpdateStudent class.
    if student_id not in students:
        return {"Error": "Student does not exist"}

    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]


# We can delete the student information.
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    del students[student_id]
    return {"Message": " Student deleted successfully"}