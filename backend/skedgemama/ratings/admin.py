from django.contrib import admin
from .models import Professor, Course, Rating, ProfGrade

# Register your models here.
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(ProfGrade)