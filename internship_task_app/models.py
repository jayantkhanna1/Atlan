from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)

class Form(models.Model):
    form_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form_description = models.CharField(max_length=100)
    form_data = models.JSONField()
    creation_time = models.DateTimeField(auto_now=True)
    
class Responses(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    response = models.JSONField()
    