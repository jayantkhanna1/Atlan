from django.contrib import admin
from .models import User, Form, Responses
# Register your models here.

admin.site.register(User)
admin.site.register(Form)
admin.site.register(Responses)