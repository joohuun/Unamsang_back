from rest_framework import serializers
from .models import Article as ArticleModel
from .models import Comment as CommentModel

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # 유저시리얼라이저 안 씀

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = CommentModel
        fields = ['user', 'comment']



class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source="comment_set", read_only=True)


    class Meta:
        model = ArticleModel
        fields = ['title', 'user','comments', 'is_active', 'exposure_end_date', 'image_location', 'image']