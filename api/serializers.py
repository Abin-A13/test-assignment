from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        if not value:
            print("validate..", value)
            raise serializers.ValidationError(
                "Name must be a non-empty string.")
        return value

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be between 0 and 120")
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            print("validation In")
            raise serializers.ValidationError("Email address must be unique.")
        return value
