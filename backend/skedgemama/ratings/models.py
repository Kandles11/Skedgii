from django.db import models

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    def __str__(self):
        return str(self.rating)
    
class SectionGrade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    grade = models.FloatField()
    def __str__(self):
        return self.grade
