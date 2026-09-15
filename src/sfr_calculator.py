from src.nba_rules import (
    calculate_total_students,
    calculate_sfr,
    calculate_average_sfr,
    calculate_sfr_marks,
)


def calculate_yearly_sfr(student_df, faculty_df, academic_year):
    """
    Calculate SFR for one academic year.
    """

    students = student_df[student_df["academic_year"] == academic_year]

    faculty = faculty_df[faculty_df["academic_year"] == academic_year]

    ug2 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 2)
    ]["student_count"].sum()

    ug3 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 3)
    ]["student_count"].sum()

    ug4 = students[
        (students["program_type"] == "UG") & (students["year_of_study"] == 4)
    ]["student_count"].sum()

    pg1 = students[
        (students["program_type"] == "PG") & (students["year_of_study"] == 1)
    ]["student_count"].sum()

    pg2 = students[
        (students["program_type"] == "PG") & (students["year_of_study"] == 2)
    ]["student_count"].sum()

    total_students = calculate_total_students(ug2, ug3, ug4, pg1, pg2)

    eligible_faculty = faculty[
        (faculty["full_time"] == "Yes")
        & (faculty["first_year_faculty"] == "No")
        & (faculty["association"].isin(["Regular", "Contractual"]))
    ]

    faculty_count = len(eligible_faculty)

    sfr = calculate_sfr(total_students, faculty_count)

    return {
        "academic_year": academic_year,
        "ug2_students": int(ug2),
        "ug3_students": int(ug3),
        "ug4_students": int(ug4),
        "pg1_students": int(pg1),
        "pg2_students": int(pg2),
        "total_students": int(total_students),
        "faculty_count": int(faculty_count),
        "sfr": round(sfr, 2),
    }


def calculate_three_year_sfr(student_df, faculty_df):
    """
    Calculate SFR for CAY, CAYm1, and CAYm2,
    then calculate average SFR and marks.
    """

    academic_years = ["CAY", "CAYm1", "CAYm2"]

    yearly_results = {}

    for year in academic_years:
        yearly_results[year] = calculate_yearly_sfr(student_df, faculty_df, year)

    sfr_values = [
        yearly_results["CAY"]["sfr"],
        yearly_results["CAYm1"]["sfr"],
        yearly_results["CAYm2"]["sfr"],
    ]

    average_sfr = calculate_average_sfr(sfr_values[0], sfr_values[1], sfr_values[2])

    marks = calculate_sfr_marks(average_sfr)

    return {
        "yearly_results": yearly_results,
        "average_sfr": round(average_sfr, 2),
        "marks": marks,
    }
