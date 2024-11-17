from django.http import JsonResponse
from django.views import View
from .models import Professor, Rating, Course, ProfGrade
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import requests
import environ


env = environ.Env()
environ.Env.read_env()

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@method_decorator(csrf_exempt, name='dispatch')

class JSONEndpointView(View):
    
    def get(self, request, *args, **kwargs):
        # Example GET response
        response_data = {
            "message": "This is a GET response.",
            "data": {"info": "Provide some JSON or check the endpoint details."}
        }
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            print("HI COLIN")
            print(data)
            rateClasses(data)
            response_data = {
                "message": "Received POST data successfully.",
                "received_data": data,
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

def parse_course(course_string):
    subject, rest = course_string.split(";;")
    course_code, course_id = rest.split("@")
    return {"subject": subject, "code": course_code, "class_id": course_id}

def fetch_professor_data(professor_id):
    API_ROOT = 'https://api.utdnebula.com/'
    path = f'professor/{professor_id}'
    response = requests.get(f'{API_ROOT}/{path}', headers={
        'x-api-key': env('NEBULA_API'),
        'Accept': 'application/json',
    })
    data = json.loads(response.text)['data']
    return data

def fetch_section_data(section_id):
    API_ROOT = 'https://api.utdnebula.com/'
    path = 'section'
    params = {'academic_session.name':'25S', "internal_class_number": section_id}
    response = requests.get(f'{API_ROOT}/{path}', headers={
        'x-api-key': env('NEBULA_API'),
        'Accept': 'application/json',
    }, params=params)
    data = json.loads(response.text)['data']
    return data

def fetch_course_data(course_id):
    API_ROOT = 'https://api.utdnebula.com/'
    path = f'course/{course_id}'
    response = requests.get(f'{API_ROOT}/{path}', headers={
        'x-api-key': env('NEBULA_API'),
        'Accept': 'application/json',
    })
    data = json.loads(response.text)['data']
    return data

def rateClasses(data):
    #turn string into dict
    formatted_data = [[parse_course(course) for course in group] for group in data]
    
    for schedule in formatted_data:
        for course in schedule:
            class_id = course["class_id"]
            section = fetch_section_data(class_id)
            print(section)
            professor = None
            myprof = None
            if not len(section[0]['professors']) == 0:
                professor = fetch_professor_data(section[0]['professors'][0])
                myprof = Professor.objects.filter(first_name=professor['first_name'], last_name=professor['last_name']).first()
                if myprof:
                    rating_instance = Rating.objects.filter(professor=myprof).first()
                    if rating_instance:
                        rmp = rating_instance.rating
                        print(rmp)
                    else:
                        print("No rating found for the professor.")
                else:
                    print("No professor found.")
            course = fetch_course_data(section[0]['course_reference'])
            internal_course_number = course['internal_course_number']
            mycourse = Course.objects.filter(internal_number=internal_course_number).first()
            if myprof and mycourse:
                mygrade = ProfGrade.objects.filter(course=mycourse, professor=myprof).first()
                print(str(mygrade.grade)) 
                finalhueristic = (rmp + mygrade.grade)   
                print("FINAL SCORE:", finalhueristic)      
            
        print(schedule)
    

