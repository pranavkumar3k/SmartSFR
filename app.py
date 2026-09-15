from io import BytesIO

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.sfr_calculator import calculate_three_year_sfr

app = FastAPI(
    title="SmartSFR API",
    description="Backend API for Student-Faculty Ratio analysis",
    version="1.0.0",
)


# Allows the local React/Lovable frontend to call this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "SmartSFR backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    student_file: UploadFile = File(...), faculty_file: UploadFile = File(...)
):
    try:
        student_content = await student_file.read()
        faculty_content = await faculty_file.read()

        student_df = pd.read_csv(BytesIO(student_content))

        faculty_df = pd.read_csv(BytesIO(faculty_content))

        required_student_columns = {
            "academic_year",
            "program",
            "program_type",
            "year_of_study",
            "student_count",
        }

        required_faculty_columns = {
            "academic_year",
            "faculty_id",
            "designation",
            "association",
            "full_time",
            "first_year_faculty",
        }

        missing_student_columns = required_student_columns - set(student_df.columns)

        missing_faculty_columns = required_faculty_columns - set(faculty_df.columns)

        if missing_student_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Student CSV is missing required columns.",
                    "missing_columns": list(missing_student_columns),
                },
            )

        if missing_faculty_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Faculty CSV is missing required columns.",
                    "missing_columns": list(missing_faculty_columns),
                },
            )

        result = calculate_three_year_sfr(student_df, faculty_df)

        return result

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Unable to analyze files: {str(error)}"
        )
