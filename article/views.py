from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import ArticleSerializer

# Create your views here.
class ArticleView(APIView):

    def get(self, request):
        user =request.user
        article_serializer = ArticleSerializer(data = request.data)

        return Response(article_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({'message': 'post입니다'})

    def put(self, request):
        return Response({'message': 'put입니다'})
        
    def delete(self, request):
        return Response({'message': 'delete입니다'})