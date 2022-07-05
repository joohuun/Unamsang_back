from rest_framework import serializers
from article.serializers import ArticleSerializer
from article.serializers import CommentSerializer
from user.models import User as UserModel


class MypageSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(many=True, source='article_set', read_only=True)
    comment = CommentSerializer(many=True, source='comment_set', read_only=True)
    class Meta:
        model = UserModel
        fields = ["username", "email", "created_at", "updated_at", "article", "comment"]
    


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
        fields = ["username", "email", "created_at", "updated_at"]
