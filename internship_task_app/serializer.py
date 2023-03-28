from rest_framework import serializers

from .models import User,Form,Responses

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'

class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        fields = '__all__'