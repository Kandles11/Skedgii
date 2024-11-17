from django.core.management.base import BaseCommand
from ratings.models import Course, ProfGrade, Professor
import environ
import requests
import json

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    help = 'Get data from the API and store it in the database'
    
    API_ROOT = 'https://trends.utdnebula.com/'
    path = 'api/combo'
    params = {}
    
    def calculate_grade(self, grade_distribution):
        # Grading scale
        grade_scale = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.666,
            "B+": 3.333,
            "B": 3.0,
            "B-": 2.666,
            "C+": 2.333,
            "C": 2.0,
            "C-": 1.666,
            "D+": 1.333,
            "D": 1.0,
            "D-": 0.666,
            "F": 0.0,
            "Withdrawal": None,  # Withdrawal grades are excluded from GPA calculation
        }

        # Map grades to the scale
        grade_keys = list(grade_scale.keys())
        total_points = 0
        total_students = 0

        for i, count in enumerate(grade_distribution):
            if grade_keys[i] != "Withdrawal" and count > 0:  # Exclude withdrawals
                total_points += count * grade_scale[grade_keys[i]]
                total_students += count

        # Calculate the average GPA
        average_gpa = total_points / total_students if total_students > 0 else 0
        return average_gpa
    
    def handle(self, *args, **kwargs):
        
        courses = Course.objects.filter(id__gte=1950)
        
        for course in courses:
            subject = course.subject
            number = course.number
            
            params = {'input':f'{subject} {number}'}

            response = requests.get(f'{self.API_ROOT}/{self.path}', headers={
            'Accept': 'application/json',
            }, params=params)

            
            if response.status_code != 200:
                print(f"API request failed with status code {response.status_code}")
                continue

            try:
                response_data = json.loads(response.text)
                data = response_data.get('data')
            except json.JSONDecodeError:
                print("Failed to parse JSON response")
                print(response.text)
                continue

            if not data:
                print(f"No 'data' key in the response for {subject} {number}")
                continue

            if data == 'mongo: no documents in result':
                print("No data found.")
                return
        
            for prof in data:
                first_name = prof['profFirst']
                last_name = prof['profLast']
                professor = Professor.objects.filter(first_name=first_name, last_name=last_name).first()
                
                myParams = {'prefix':str(subject),'number':str(number), 'profFirst': first_name, 'profLast': last_name}
                print(myParams)
                
                response = requests.get(f'{self.API_ROOT}api/grades', headers={
            'Accept': 'application/json',
            }, params=myParams)
                print(response.request.url)
                
                print(response.text)
                data = json.loads(response.text)['data']
                print(data)
                
                profAverageGPA = 0
                if data:
                    for semesterGrades in data:
                        gradeDistribution = semesterGrades['grade_distribution']
                        averageGPA = self.calculate_grade(gradeDistribution)
                        profAverageGPA += averageGPA
                else:
                    print(f"No grades found for {first_name} {last_name} in {subject} {number}")
                    profAverageGPA = None

                if profAverageGPA is not None:
                    profAverageGPA = profAverageGPA / len(data) if len(data) > 0 else 0
                else:
                    profAverageGPA = None
                print(f"Average GPA for {first_name} {last_name} in {subject} {number}: {profAverageGPA}")
            
                try:
                    if profAverageGPA is not None:
                        classGrade = ProfGrade.objects.create(course=course, professor=professor, grade=profAverageGPA)
                        classGrade.save()
                        print(f'Course {classGrade} created')
                except Exception as e:
                    print(f"Error saving course {subject} {number}: {e}")
        

    