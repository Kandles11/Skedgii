from django.core.management.base import BaseCommand
from ratings.models import Course
import environ
import requests
import json

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    help = 'Get data from the API and store it in the database'
    
    API_ROOT = 'https://api.utdnebula.com/'
    path = 'course/all'
    params = {}

    
    def handle(self, *args, **kwargs):
        response = requests.get(f'{self.API_ROOT}/{self.path}', headers={
            'x-api-key': env('NEBULA_API'),
            'Accept': 'application/json',
        }, params=self.params)
        data = json.loads(response.text)['data']

        if data == 'mongo: no documents in result':
            print("No data found.")
            return
        
        for course in data:
            if course['catalog_year'] == '24':
                title = course['title']
                number = course['course_number']
                subject = course['subject_prefix']
                internal_number = course['internal_course_number']
                print(f"Processing course {title} ({internal_number})")
                try:
                    course_obj = Course.objects.create(title=title, number=number, subject=subject, internal_number=internal_number)
                    course_obj.save()
                    print(f'Course {course_obj} created')
                except Exception as e:
                    print(f"Error saving course {title} {internal_number}: {e}")
        

    