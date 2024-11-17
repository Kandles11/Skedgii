import logging
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

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@method_decorator(csrf_exempt, name="dispatch")
class JSONEndpointView(View):
    def get(self, request, *args, **kwargs):
        # Example GET response
        response_data = {
            "message": "This is a GET response.",
            "data": {"info": "Provide some JSON erm sigma int details."},
        }
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            logging.info("Received POST request with data: %s", data)

            results = rate_classes(data)

            response_data = {
                "message": "Processed POST data successfully.",
                "results": results,
            }
            logging.info("POST request processing complete. Returning results.")
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            logging.error("Invalid JSON data in POST request.")
            return JsonResponse({"error": "Invalid JSON data."}, status=400)


def parse_course(course_string):
    subject, rest = course_string.split(";;")
    course_code, course_id = rest.split("@")
    return {"subject": subject, "code": course_code, "class_id": course_id}


def fetch_professor_data(professor_id, cache):
    if professor_id in cache["professors"]:
        logging.info("Cache hit for professor_id: %s", professor_id)
        return cache["professors"][professor_id]

    logging.info("Cache miss for professor_id: %s. Fetching data from API.", professor_id)
    API_ROOT = "https://api.utdnebula.com/"
    path = f"professor/{professor_id}"
    response = requests.get(
        f"{API_ROOT}/{path}",
        headers={
            "x-api-key": env("NEBULA_API"),
            "Accept": "application/json",
        },
    )
    data = json.loads(response.text)["data"]
    cache["professors"][professor_id] = data
    return data


def fetch_section_data(section_id, cache):
    if section_id in cache["sections"]:
        logging.info("Cache hit for section_id: %s", section_id)
        return cache["sections"][section_id]

    logging.info("Cache miss for section_id: %s. Fetching data from API.", section_id)
    API_ROOT = "https://api.utdnebula.com/"
    path = "section"
    params = {"academic_session.name": "25S", "internal_class_number": section_id}
    response = requests.get(
        f"{API_ROOT}/{path}",
        headers={
            "x-api-key": env("NEBULA_API"),
            "Accept": "application/json",
        },
        params=params,
    )
    data = json.loads(response.text)["data"]
    cache["sections"][section_id] = data
    return data


def fetch_course_data(course_id, cache):
    if course_id in cache["courses"]:
        logging.info("Cache hit for course_id: %s", course_id)
        return cache["courses"][course_id]

    logging.info("Cache miss for course_id: %s. Fetching data from API.", course_id)
    API_ROOT = "https://api.utdnebula.com/"
    path = f"course/{course_id}"
    response = requests.get(
        f"{API_ROOT}/{path}",
        headers={
            "x-api-key": env("NEBULA_API"),
            "Accept": "application/json",
        },
    )
    data = json.loads(response.text)["data"]
    cache["courses"][course_id] = data
    return data


def rate_classes(data):
    results = []
    cache = {"professors": {}, "sections": {}, "courses": {}}

    for schedule in data:
        schedule_id = schedule["id"]
        combinations = schedule["combination"]
        logging.info("Processing schedule ID: %s with combinations: %s", schedule_id, combinations)

        parsed_courses = [parse_course(course) for course in combinations]

        total_heuristic = 0

        for course in parsed_courses:
            class_id = course["class_id"]
            logging.info("Processing course with class_id: %s", class_id)

            section = fetch_section_data(class_id, cache)
            professor = None
            myprof = None
            rmp = 0

            if section and section[0].get("professors"):
                professor_id = section[0]["professors"][0]
                professor_data = fetch_professor_data(professor_id, cache)
                myprof = Professor.objects.filter(
                    first_name=professor_data["first_name"],
                    last_name=professor_data["last_name"],
                ).first()

                if myprof:
                    rating_instance = Rating.objects.filter(professor=myprof).first()
                    if rating_instance:
                        rmp = rating_instance.rating
                        logging.info("Found RMP rating: %s for professor: %s", rmp, professor_data)

            course_data = fetch_course_data(section[0]["course_reference"], cache)
            internal_course_number = course_data["internal_course_number"]
            mycourse = Course.objects.filter(
                internal_number=internal_course_number
            ).first()

            course_heuristic = rmp
            if myprof and mycourse:
                mygrade = ProfGrade.objects.filter(
                    course=mycourse, professor=myprof
                ).first()
                if mygrade:
                    course_heuristic += mygrade.grade
                    logging.info(
                        "Added grade: %s for course: %s and professor: %s",
                        mygrade.grade,
                        mycourse,
                        myprof,
                    )

            total_heuristic += course_heuristic

        # Add heuristic and original combination to results
        logging.info("Total heuristic for schedule ID %s: %s", schedule_id, total_heuristic)
        results.append(
            {"id": schedule_id, "heuristic": total_heuristic, "combination": combinations}
        )

    # Sort results by heuristic in descending order
    sorted_results = sorted(results, key=lambda x: x["heuristic"], reverse=True)
    logging.info("Final sorted results: %s", sorted_results)
    return sorted_results

@method_decorator(csrf_exempt, name="dispatch")
class PuckEndpoint(View):
     def get(self, request, *args, **kwargs):
        # Example GET response
        response_data = {
            "message": "This is a GET response.",
            "data": {"classOpen": True},
        }
        return JsonResponse(response_data)