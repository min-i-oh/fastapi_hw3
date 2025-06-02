from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

GRADE_TO_SCORE = {
    "A+": 4.5, "A0": 4.0,
    "B+": 3.5, "B0": 3.0,
    "C+": 2.5, "C0": 2.0,
    "D+": 1.5, "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentData(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/score")
def calculate_gpa(data: StudentData):
    total_credits = sum(course.credits for course in data.courses)
    total_points = sum(GRADE_TO_SCORE[course.grade] * course.credits for course in data.courses)
    gpa = round(total_points / total_credits, 2)
    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
