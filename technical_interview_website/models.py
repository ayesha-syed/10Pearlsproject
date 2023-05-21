from django.db import models

# Create your models here.
class videos(models.Model):
    video=models.FileField(upload_to="video/")



class Candidate(models.Model):
    first_Name = models.CharField(max_length=20,null=True)
    last_Name = models.CharField(max_length=20,null=True)
    username = models.CharField(max_length=20,unique=True,null=False,blank=False)
    email = models.EmailField(max_length=40,unique=True,null=False,blank=False)
    password = models.CharField(max_length=20,null=False,blank=False)
    Position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.email

class Interview(models.Model):
    candidate_id=models.ForeignKey('Candidate',on_delete=models.CASCADE)
    admin_id=models.ForeignKey('Admin',on_delete=models.CASCADE)
    interview_deadline=models.DateField()
    interview_video=models.FileField(null=True,blank=True)
    feedback = models.TextField(max_length=100, null=True)
    interview_email=models.CharField(max_length=1000)
    Questionnaire=models.ForeignKey('Questionnaire',on_delete=models.SET_NULL,null=True)
    Status=models.BooleanField(default=False)
    def __str__(self):
        return (str(self.admin_id)+"-"+str(self.candidate_id))

class Position(models.Model):
    position = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.position

class Questionnaire(models.Model):
    Questionnaire_name = models.CharField(max_length=50,unique=True)
    questions = models.ManyToManyField("ActualQuestion")

    def __str__(self):
        return self.Questionnaire_name

class Admin(models.Model):
    first_Name = models.CharField(max_length=20,blank=False)
    last_Name = models.CharField(max_length=20,blank=False)
    email = models.EmailField(max_length=40,unique=True,blank=False)
    password = models.CharField(max_length=20,blank=False)
    def __str__(self):
        return self.email

class ActualQuestion(models.Model):
    Actual_Question = models.TextField(max_length=1000,unique=True)
    def __str__(self):
        return self.Actual_Question

