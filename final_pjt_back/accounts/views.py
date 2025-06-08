from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import UserDetailsView
from dj_rest_auth.registration.views import RegisterView
from .serializers import (
    UserSurveySerializer,
    UserProfileSerializer,
    CustomUserDetailsSerializer, CustomRegisterSerializer
)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

# 회원 정보 조회 (이름, 닉네임, 이메일 등)
class CustomUserDetailView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticated]


# 설문 저장
class UserSurveyView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserSurveySerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "설문이 저장되었습니다."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 마이페이지 프로필 조회 및 수정
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필이 수정되었습니다."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴
class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
