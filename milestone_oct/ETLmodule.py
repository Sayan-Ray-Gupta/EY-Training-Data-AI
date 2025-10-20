import pandas as pd

def run_etl(processed_path='processed_enrollments.csv'):
    # Load required files
    df_students = pd.read_csv('students.csv')
    df_courses = pd.read_csv('courses.csv')
    df_enrollments = pd.read_csv(processed_path, parse_dates=['EnrollDate'])

    # Join and enrich data
    merged = df_enrollments.merge(df_students, on='StudentID', how='left')
    merged = merged.merge(df_courses, on='CourseID', how='left')

    merged['CompletionStatus'] = merged['Progress'].apply(lambda x: 'Completed' if x >= 80 else 'In Progress')
    merged['EnrollMonth'] = pd.to_datetime(merged['EnrollDate']).dt.strftime('%Y-%m')

    # Save full processed data
    processed = merged[[
        'EnrollmentID', 'StudentID', 'Name', 'Email', 'Country',
        'CourseID', 'Title', 'Category', 'Duration',
        'EnrollDate', 'EnrollMonth', 'Progress', 'CompletionStatus'
    ]]
    processed.to_csv(processed_path, index=False)

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

    # Monthly trends
    monthly_trends = processed.groupby('EnrollMonth').size().reset_index(name='Enrollments')
    monthly_trends.to_csv('reports/monthly_enrollment_trends.csv', index=False)

    # Combined report
    report = pd.concat([completion, students_per_category, country_enrollments, monthly_trends], ignore_index=True, sort=False)
    report.to_csv('reports/learning_analytics.csv', index=False)

    print("ETL completed and analytics updated.")
