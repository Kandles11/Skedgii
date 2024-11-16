from django.core.management.base import BaseCommand
from ratings.models import Professor, Rating
import environ
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    help = 'Get data from the API and store it in the database'
    
    API_ROOT = 'https://api.utdnebula.com/'
    path = 'professor/all'
    params = {}

    def fetch_professor_data(self, professor):
        """Fetch and process individual professor data."""
        first_name = professor['first_name']
        last_name = professor['last_name']
        
        try:
            response = requests.get('https://trends.utdnebula.com/api/ratemyprofessorScraper', headers={
            'x-api-key': env('NEBULA_API'),
            'Accept': 'application/json',
            }, params={'profFirst': first_name, 'profLast': last_name})
            prof_rating = json.loads(response.text)['data']['avgRating']
        except Exception as e:
            print(f"Error fetching rating for {first_name} {last_name}: {e}")
            prof_rating = None
        
        try:
            professor_obj = Professor.objects.create(first_name=first_name, last_name=last_name)
            professor_obj.save()
            if prof_rating is not None:
                Rating.objects.create(professor=professor_obj, rating=prof_rating)
            print(f'Professor {professor_obj} created with rating {prof_rating}')
        except Exception as e:
            print(f"Error saving professor {first_name} {last_name}: {e}")
    
    def handle(self, *args, **kwargs):
        response = requests.get(f'{self.API_ROOT}/{self.path}', headers={
            'x-api-key': env('NEBULA_API'),
            'Accept': 'application/json',
        }, params=self.params)
        data = json.loads(response.text)['data']

        if data == 'mongo: no documents in result':
            print("No data found.")
            return
        
        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.fetch_professor_data, professor) for professor in data]
            for future in as_completed(futures):
                try:
                    future.result()  # Raise exceptions if any occurred
                except Exception as e:
                    print(f"Error processing professor: {e}")
