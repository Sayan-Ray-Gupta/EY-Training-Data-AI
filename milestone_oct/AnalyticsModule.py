import pandas as pd

df = pd.read_csv('processed_enrollments.csv', parse_dates=['EnrollDate'])

# Completion rate per course
completion = df.groupby('CourseID').apply(
    lambda x: (x['Progress'] >= 80).mean() * 100
).reset_index(name='CompletionRate(%)')
completion.to_csv('reports/completion_rate_per_course.csv', index=False)

# Total students per category
students_per_category = df.groupby('Category')['StudentID'].nunique().reset_index(name='TotalStudents')  # unique count
students_per_category.to_csv('reports/total_students_per_category.csv', index=False)


# Country wise enrollment
country_enrollments = df.groupby('Country').size().reset_index(name='Enrollments')
country_enrollments.to_csv('reports/country_wise_enrollments.csv', index=False)

# Monthly Enrollment Trends
df['EnrollMonth'] = df['EnrollDate'].dt.to_period('M')
monthly_trends = df.groupby('EnrollMonth').size().reset_index(name='Enrollments')
monthly_trends['EnrollMonth'] = monthly_trends['EnrollMonth'].dt.strftime('%Y-%m')
monthly_trends.to_csv('reports/monthly_enrollment_trends.csv', index=False)


report = pd.concat([completion, students_per_category, country_enrollments, monthly_trends], ignore_index=True, sort=False)

report.to_csv('reports/learning_analytics.csv', index=False)
print("Analytics saved to reports/learning_analytics.csv")
