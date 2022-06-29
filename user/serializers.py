from rest_framework import serializers
from user.models import User as UserModel

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ["username", "email", "created_at", "updated_at"]
