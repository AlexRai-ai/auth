# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
      model = CustomUser
      fields = ['email', 'mobile']

  def create(self, validated_data):
      return CustomUser.objects.create_user(**validated_data)