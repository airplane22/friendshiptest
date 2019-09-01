from django.db import models

# Create your models here.

class Quiz(models.Model):
    quiz = models.CharField(max_length=200)
    answer1 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)

class MainUser(models.Model):
    username = models.CharField(max_length=10)
    code = models.IntegerField()
    url = models.CharField(max_length=200)

    quiz = models.ManyToManyField(Quiz, through='UserQuiz')



class UserQuiz(models.Model):
    mainuser = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    quiz_num = models.IntegerField()
    answer = models.IntegerField()

class SubUser(models.Model):
    mainuser = models.ForeignKey(MainUser, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)