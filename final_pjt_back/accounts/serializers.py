# accounts/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User
from products.models import Scrap
from products.serializers import DepositSerializer, SavingSerializer

# 1. 회원가입용 Serializer
class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def save(self, request):
        print("🔥🔥🔥 CustomRegisterSerializer save() 호출됨")
        print("🔥 validated_data:", self.validated_data)
        
        user = super().save(request)
        user.name = self.validated_data.get('name')
        user.nickname = self.validated_data.get('nickname')
        user.profile_image = self.validated_data.get('profile_image', None)
        user.save()
        print('회원가입 validated_data:', self.validated_data)
        return user


class UserScrapSerializer(serializers.ModelSerializer):
    deposit = DepositSerializer(read_only=True)
    saving = SavingSerializer(read_only=True)

    class Meta:
        model = Scrap
        fields = ['id', 'deposit', 'saving', 'created_at']
        

# 2. 회원정보 조회/수정 Serializer
class CustomUserDetailsSerializer(UserDetailsSerializer):
    scraps = UserScrapSerializer(many=True, read_only=True)
    
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + ('name', 'nickname', 'profile_image', 'scraps')
        read_only_fields = ('email', 'username')  # 수정 방지



# 3. 설문 저장용 Serializer
class UserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'age_group',
            'job',
            'income_level',
            'consumption_type',
            'saving_goal',
            'saving_period',
            'monthly_saving_amount',
            'preference_tags',
        ]


# 4. 마이페이지 조회 및 수정용 Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'user_permissions', 'groups']
        read_only_fields = ['username', 'email', 'date_joined'] # 수정 불가

