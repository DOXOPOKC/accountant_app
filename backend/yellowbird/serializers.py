from rest_framework import serializers
from .models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', ]
