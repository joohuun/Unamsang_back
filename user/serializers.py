from rest_framework import serializers
from user.models import User as UserModel

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "created_at", "updated_at"]
