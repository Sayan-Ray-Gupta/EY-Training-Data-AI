import pandas as pd
import logging


# Set up logging
logging.basicConfig(
    filename='log.app',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)


def run_etl(processed_path='processed_enrollments.csv'):
    try:
        # Load files
        df_students = pd.read_csv('students.csv')
        df_courses = pd.read_csv('courses.csv')
        df_enrollments = pd.read_csv(processed_path, parse_dates=['EnrollDate'])

        # Validate student file columns
        required_student_cols = {'StudentID', 'Name', 'Email', 'Country'}
        if not required_student_cols.issubset(df_students.columns):
            missing = required_student_cols - set(df_students.columns)
            raise ValueError(f"Missing columns in students.csv: {missing}")

        # Validate course file columns
        required_course_cols = {'CourseID', 'Title', 'Category', 'Duration'}
        if not required_course_cols.issubset(df_courses.columns):
            missing = required_course_cols - set(df_courses.columns)
            raise ValueError(f"Missing columns in courses.csv: {missing}")

        # Drop overlapping columns from enrollments before merging
        overlap_cols = ['Name', 'Email', 'Country', 'Title', 'Category', 'Duration']
        df_enrollments_clean = df_enrollments.drop(columns=[col for col in overlap_cols if col in df_enrollments.columns])

        # Select only necessary columns from students and courses to merge
        df_students_trimmed = df_students[['StudentID', 'Name', 'Email', 'Country']]
        df_courses_trimmed = df_courses[['CourseID', 'Title', 'Category', 'Duration']]

        # Merge enrollments with students and courses
        merged = df_enrollments_clean.merge(df_students_trimmed, on='StudentID', how='left')
        merged = merged.merge(df_courses_trimmed, on='CourseID', how='left')

        # Debug: print merged columns
        print("[ETL] Columns in merged DataFrame:", merged.columns.tolist())
        logging.info(f"[ETL] Merged DataFrame columns: {merged.columns.tolist()}")

        # Create derived columns
        merged['CompletionStatus'] = merged['Progress'].apply(lambda x: 'Completed' if x >= 80 else 'In Progress')
        merged['EnrollMonth'] = pd.to_datetime(merged['EnrollDate']).dt.strftime('%Y-%m')

        # Define the expected columns to output
        expected_cols = [
            'EnrollmentID', 'StudentID', 'Name', 'Email', 'Country',
            'CourseID', 'Title', 'Category', 'Duration',
            'EnrollDate', 'EnrollMonth', 'Progress', 'CompletionStatus'
        ]

        # Check for missing expected columns
        missing_cols = [col for col in expected_cols if col not in merged.columns]
        if missing_cols:
            raise ValueError(f"Missing expected columns in merged data: {missing_cols}")

        # Save cleaned and enriched data back to processed_path
        processed = merged[expected_cols]
        processed.to_csv(processed_path, index=False)

        # === Generate reports ===

        # Completion rate per course
        completion = processed.groupby('CourseID').apply(
            lambda x: (x['Progress'] >= 80).mean() * 100
        ).reset_index(name='CompletionRate(%)')
        completion.to_csv('reports/completion_rate_per_course.csv', index=False)

        # Total students per category
        students_per_category = processed.groupby('Category')['StudentID'].nunique().reset_index(name='TotalStudents')
        students_per_category.to_csv('reports/total_students_per_category.csv', index=False)

        # Country-wise enrollments
        country_enrollments = processed.groupby('Country').size().reset_index(name='Enrollments')
        country_enrollments.to_csv('reports/country_wise_enrollments.csv', index=False)

        # Monthly enrollment trends
        monthly_trends = processed.groupby('EnrollMonth').size().reset_index(name='Enrollments')
        monthly_trends.to_csv('reports/monthly_enrollment_trends.csv', index=False)

        # Combined report (optional)
        report = pd.concat([
            completion,
            students_per_category,
            country_enrollments,
            monthly_trends
        ], ignore_index=True, sort=False)
        report.to_csv('reports/learning_analytics.csv', index=False)

        print("ETL completed and reports updated.")
        logging.info("[ETL] ETL process completed successfully.")

    except Exception as e:
        logging.error(f"[ETL] Error during ETL: {str(e)}")
        print("ETL Error:", e)
