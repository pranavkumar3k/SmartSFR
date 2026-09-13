# src/sfr_calculator.py

"""
SFR Calculator

Reads student and faculty data from DataFrames
and applies NBA Section 4.1 formulas.
"""

import pandas as pd

from nba_rules import (
    calculate_total_students,
    calculate_sfr,
    calculate_average_sfr,
    calculate_sfr_marks,
)


def calculate_yearly_sfr(student_df, faculty_df, academic_year):
    """
    Calculate SFR for one academic year.

    Parameters:
        student_df: DataFrame containing student data
        faculty_df: DataFrame containing faculty data
        academic_year: CAY, CAYm1, or CAYm2

    Returns:
        Dictionary containing S, F, and SFR.
    """

    # Filter data for the selected academic year
    students = student_df[student_df["academic_year"] == academic_year]

    faculty = faculty_df[faculty_df["academic_year"] == academic_year]

    # Calculate student totals according to NBA categories
    ug1 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 2)
    ]["student_count"].sum()

    ug2 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 3)
    ]["student_count"].sum()

    ug3 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 4)
    ]["student_count"].sum()

    pg1 = students[
        (students["program_type"] == "PG") & (students["year_of_study"] == 1)
    ]["student_count"].sum()

    pg2 = students[
        (students["program_type"] == "PG") & (students["year_of_study"] == 2)
    ]["student_count"].sum()

    # Total students according to NBA formula
    total_students = calculate_total_students(ug1, ug2, ug3, pg1, pg2)

    # Faculty eligibility rules
    eligible_faculty = faculty[
        (faculty["full_time"] == "Yes")
        & (faculty["first_year_faculty"] == "No")
        & (faculty["association"].isin(["Regular", "Contractual"]))
    ]

    faculty_count = len(eligible_faculty)

    # Calculate SFR
    sfr = calculate_sfr(total_students, faculty_count)

    return {
        "academic_year": academic_year,
        "ug1": ug1,
        "ug2": ug2,
        "ug3": ug3,
        "pg1": pg1,
        "pg2": pg2,
        "total_students": total_students,
        "faculty_count": faculty_count,
        "sfr": sfr,
    }


def calculate_three_year_sfr(student_df, faculty_df):
    """
    Calculate SFR for CAY, CAYm1, and CAYm2.
    """

    years = ["CAY", "CAYm1", "CAYm2"]

    results = {}

    for year in years:
        results[year] = calculate_yearly_sfr(student_df, faculty_df, year)

    sfr_values = [
        results["CAY"]["sfr"],
        results["CAYm1"]["sfr"],
        results["CAYm2"]["sfr"],
    ]

    average_sfr = calculate_average_sfr(*sfr_values)

    marks = calculate_sfr_marks(average_sfr)

    return {"yearly_results": results, "average_sfr": average_sfr, "marks": marks}
