from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article as ArticleModel
from django.db.models.query_utils import Q
from v_diffusion_pytorch.image_gen import run
import os
from rest_framework_simplejwt.authentication import JWTAuthentication


class ImageGenerationView(APIView):
    def post(self, request):
        prompt = request.data["prompt"]
        print("****************")
        print(prompt)
        print("****************")
        header_of_filename = run(request.user.username, prompt)
        images = []
        for i in range(4):
            images.append(f'media/images/{header_of_filename}_{i}.png')
        images.append(f'media/images/{header_of_filename}_finalgrid.png')

        image = f'media/images/{header_of_filename}'

        return Response({"msg": "Success", "images": image, "title": prompt})

    def delete(self, request, images):
        for image in images:
            os.remove(image)
        return Response({"msg": "delete success"})


class ArticleView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        articles = ArticleModel.objects.all()
        articles_count = articles.count()
        article_serializer = ArticleSerializer(articles, many=True)
        article_serializer.data.append(('articles_count', articles_count))

        # article_serializer.data['articles_count']=articles_count
        print(article_serializer.data)

        return Response(article_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        global header_of_filename

        article_serializer = ArticleSerializer(data=request.data)
        # print(f'serializer:{article_serializer}')
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        article_serializer = ArticleSerializer(
            article, data=request.data, partial=True)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        article.delete()

        return Response({'message': '삭제되었습니다'}, status=status.HTTP_200_OK)


class ArticleSearchView(APIView):
    def get(self, request):
        words = request.query_params.getlist('words', '')
        print("words = ", end=""), print(words)

        query = Q()
        for word in words:
            if word.strip() != "":
                query.add(Q(title__icontains=word.strip()), Q.OR)
                query.add(Q(user__username__icontains=word.strip()), Q.OR)
        articles = ArticleModel.objects.filter(query)

        if articles.exists():
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
