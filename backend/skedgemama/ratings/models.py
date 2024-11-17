from django.db import models

# Create your models here.
class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    number = models.CharField()
    subject = models.CharField(max_length=10)
    internal_number = models.CharField()
    def __str__(self):
        return self.title
    
class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.FloatField()
    def __str__(self):
        return str(self.rating)
    
class ProfGrade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    grade = models.FloatField()
    def __str__(self):
        return self.grade
