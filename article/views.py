from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

# Create your views here.
class ArticleView(APIView):

    def get(self, request):
        return Response({'message': 'Get입니다'})
    def post(self, request):
        return Response({'message': 'post입니다'})
    def put(self, request):
        return Response({'message': 'put입니다'})
    def delete(self, request):
        return Response({'message': 'delete입니다'})