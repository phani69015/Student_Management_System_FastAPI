from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from database import students_collection
from models import student_helper
from schemas import Student, StudentUpdate

app = FastAPI()

@app.post("/students", response_model=dict, status_code=201)
async def create_student(student: Student):
    student_data = student.model_dump()
    result = students_collection.insert_one(student_data) 
    if result.inserted_id:
        return {"id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Student could not be created")


@app.get("/students", response_model=dict)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}
    
    students_cursor = students_collection.find(query)
    students = [student_helper(student) for student in students_cursor]  
    return {"data": students}


@app.get("/students/{id}", response_model=dict)
async def fetch_student(id: str = Path(..., description="The ID of the student")):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    student = students_collection.find_one({"_id": ObjectId(id)})  
    if student:
        return student_helper(student)
    raise HTTPException(status_code=404, detail="Student not found")


@app.patch("/students/{id}", response_model=None, status_code=204)
async def update_student(id: str, student_update: StudentUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    update_data = {k: v for k, v in student_update.model_dump().items() if v is not None}
    if update_data:
        result = students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )   
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
    else:
        raise HTTPException(status_code=400, detail="No fields to update")


@app.delete("/students/{id}", response_model=None, status_code=200)
async def delete_student(id: str = Path(..., description="The ID of the student")):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    result = students_collection.delete_one({"_id": ObjectId(id)})  
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
