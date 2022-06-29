from rest_framework import serializers
from user.models import User as UserModel

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "created_at", "updated_at"]
