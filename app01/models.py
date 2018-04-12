from django.db import models

# Create your models here.

class Classes(models.Model):
    # id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32)

class Student(models.Model):
    name = models.CharField(max_length=32)
    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)
    cls = models.ForeignKey("Classes", on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.CharField(max_length=32)
    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)
    cls = models.ManyToManyField("Classes")         #加引号，否则会找不到。

class Administrator(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
