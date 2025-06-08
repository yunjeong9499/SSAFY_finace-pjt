from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. 연령대
AGE_GROUP_CHOICES = [
    ('10s', '10대'),
    ('20s', '20대'),
    ('30s', '30대'),
    ('40s', '40대'),
    ('50s+', '50대 이상'),
]

# 2. 직업
JOB_CHOICES = [
    ('company', '회사원'),
    ('gov', '공무원'),
    ('self', '자영업자'),
    ('freelance', '프리랜서'),
    ('student', '학생 / 무직'),
    ('etc', '기타'),
]

# 3. 소득
INCOME_LEVEL_CHOICES = [
    ('under100', '100만 원 이하'),
    ('100_300', '100~300만 원'),
    ('300_500', '300~500만 원'),
    ('over500', '500만 원 이상'),
]

# 4. 소비 성향
CONSUMPTION_CHOICES = [
    ('saving', '절약형'),
    ('flexible', '유동형'),
    ('spending', '자유소비형'),
]

# 5. 목적
GOAL_CHOICES = [
    ('emergency', '비상금 마련'),
    ('short', '여행/가전 등 단기 목표'),
    ('asset', '자산 형성'),
    ('etc', '기타'),
]

# 6. 기간
SAVING_PERIOD_CHOICES = [
    ('under6m', '6개월 미만'),
    ('6m_1y', '6개월 ~ 1년'),
    ('1y_3y', '1년 ~ 3년'),
    ('over3y', '3년 이상'),
]

# 7. 월 저축 가능 금액
MONTHLY_SAVING_CHOICES = [
    ('under10', '10만 원 이하'),
    ('10_30', '10~30만 원'),
    ('30_50', '30~50만 원'),
    ('over50', '50만 원 이상'),
]


class User(AbstractUser):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)
    
    # 설문 필드
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, blank=True)
    job = models.CharField(max_length=20, choices=JOB_CHOICES, blank=True)
    income_level = models.CharField(max_length=20, choices=INCOME_LEVEL_CHOICES, blank=True)
    consumption_type = models.CharField(max_length=20, choices=CONSUMPTION_CHOICES, blank=True)
    saving_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)
    saving_period = models.CharField(max_length=20, choices=SAVING_PERIOD_CHOICES, blank=True)
    monthly_saving_amount = models.CharField(max_length=20, choices=MONTHLY_SAVING_CHOICES, blank=True)

    # 상품 조건 선호 (복수 선택: 고금리, 모바일가입, 중도해지 가능 등)
    preference_tags = models.JSONField(null=True, blank=True)
    # 예시 저장값: ["high_interest", "easy_mobile", "free_withdraw"]

    survey_completed = models.BooleanField(default=False)
    # 추천 페이지 접근 시 user.survey_completed == True 체크 → 미완료 시 /survey/로 이동

    def __str__(self):
        return self.username


# ✅ 예시: preference_tags 저장 값
# 사용자 선택에 따라 프론트엔드에서 아래처럼 전송 가능합니다:

# {
#   "preference_tags": ["high_interest", "easy_mobile", "free_withdraw"]
# }
# 프론트에서 선택지는 다음과 같이 표시하면 좋습니다:

# 높은 금리	high_interest
# 모바일 가입 용이	easy_mobile
# 자유입출금 가능	free_withdraw
# 중도 해지 시 손실 적음	low_penalty
# 일정 기간 묶여도 괜찮음	long_term_ok