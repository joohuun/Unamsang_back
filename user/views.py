from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from user.serializers import MypageSerializer, UserSerializer
from user.models import User as UserModel

from user.serializers_jwt import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
	# JWT 인증방식 클래스 지정
    authentication_classes = [JWTAuthentication]

    # 회원 정보 조회
    def get(self, request):
		# Token에서 인증된 user만 가져옴
        user = request.user
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)

    # 회원 정보 수정
    def put(self, request, obj_id):
        user = UserModel.objects.get(id=obj_id)
        if request.user != user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(user, request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class MypageView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self, request):
        print(request.user)
        mypage_serializer = MypageSerializer(request.user).data
        print(mypage_serializer)
        return Response(mypage_serializer, status=status.HTTP_200_OK)
    

# 로그인
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    
    


    