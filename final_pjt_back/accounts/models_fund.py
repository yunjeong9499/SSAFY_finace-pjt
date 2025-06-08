from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
JOB_CHOICES = [
    ('company', '회사원'),
    ('gov', '공무원'),
    ('self', '자영업자'),
    ('freelance', '프리랜서'),
    ('student', '무직/학생'),
    ('etc', '기타'),
]

INCOME_CHOICES = [
    ('1', '100만 원 이하'),
    ('2', '100~300만 원'),
    ('3', '300~500만 원'),
    ('4', '500~700만 원'),
    ('5', '700만 원 이상'),
]

CONSUMPTION_CHOICES = [
    ('save', '절약형'),
    ('balance', '유동형'),
    ('spend', '소비형'),
]

RISK_CHOICES = [
    ('low', '저위험'),
    ('medium', '중위험'),
    ('high', '고위험'),
]

GOAL_CHOICES = [
    ('house', '내 집 마련'),
    ('retire', '노후 자금 준비'),
    ('short', '단기 목돈 마련'),
]

INVESTMENT_PERIOD_CHOICES = [
    ('6m', '6개월'),
    ('1y', '1년'),
    ('3y', '3년'),
    ('5y+', '5년 이상'),
]

EXPECTED_RETURN_CHOICES = [
    ('under3', '3% 이하'),
    ('around5', '5% 전후'),
    ('over10', '10% 이상'),
    ('over20', '20% 이상'),
]

MONTHLY_INVEST_CHOICES = [
    ('under10', '10만 원 이하'),
    ('10_30', '10~30만 원'),
    ('30_50', '30~50만 원'),
    ('over50', '50만 원 이상'),
]

class User(AbstractBaseUser):
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)

    # 설문 기반(펀드 포함)
    age = models.PositiveIntegerField(blank=True)
    job = models.CharField(max_length=20, choices=JOB_CHOICES, blank=True)
    income_level = models.CharField(max_length=20, choices=INCOME_CHOICES, blank=True)
    consumption_level = models.CharField(max_length=10, choices=CONSUMPTION_CHOICES, blank=True)
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)
    investment_period = models.CharField(max_length=10, choices=INVESTMENT_PERIOD_CHOICES, blank=True)

    # 보유 자산: 복수 선택 가능 → JSON 필드 활용
    assets_owned = models.JSONField(null=True, blank=True)
    # 예: ["예적금", "부동산", "주식/펀드"]

    expected_return = models.CharField(max_length=10, choices=EXPECTED_RETURN_CHOICES, blank=True)
    monthly_invest_amount = models.CharField(max_length=20, choices=MONTHLY_INVEST_CHOICES, blank=True)

    def __str__(self):
        return self.username


# 설문을 안 한 유저는 추천 페이지 진입 시 /survey로 리다이렉트
class Scrap(models.Model):
    pass