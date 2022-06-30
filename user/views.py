from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from user.serializers import UserSerializer
from user.models import User as UserModel

# from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class UserView(APIView):
    
    permission_classes = [permissions.AllowAny]

    # 회원 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정
    def put(self, request, obj_id):
        user = UserModel.objects.get(id=obj_id)
        user_serializer = UserSerializer(user, request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공."}, status=status.HTTP_200_OK)

    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공."}, status=status.HTTP_200_OK)

# class SpartaTokenObtainPairView(TokenObtainPairView):
#     serializer_class = SpartaTokenObtainPairSerializer

# class OnlyAuthenticatedUserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
		
# 		# JWT 인증방식 클래스 지정하기
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
# 				# Token에서 인증된 user만 가져온다.
#         user = request.user
#         print(f"user 정보 : {user}")
#         if not user:
#             return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response({"message": "Accepted"})