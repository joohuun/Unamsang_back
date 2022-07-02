from rest_framework import serializers
from .models import Article as ArticleModel
from .models import Comment as CommentModel
from .models import Rating as RatingModel
from django.db.models import Avg

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = CommentModel
        fields = "__all__"
        
        
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = RatingModel
        fields = "__all__"
        
    
class ArticleSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, source="comment_set", read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username') 
    rating = serializers.SerializerMethodField()
    def get_rating(self, obj):
        ratings = obj.rating_set
        return {
            "평균 평점":ratings.aggregate(Avg("rating"))
        }
    

    class Meta:
        model = ArticleModel
        fields = "__all__"