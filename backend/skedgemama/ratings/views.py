from django.http import JsonResponse
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

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

def rateClasses(data):
    # Example POST response
    formatted_data = [[parse_course(course) for course in group] for group in data]
    
    print(formatted_data)

