from django.db import models
from django.conf import settings

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)

class Deposit(models.Model):
    deposit_code = models.CharField(max_length=50, unique=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    join_way = models.TextField(null=True)
    mtrt_int = models.TextField(null=True)
    spcl_cnd = models.TextField(null=True)
    join_deny = models.IntegerField()
    join_member = models.TextField()
    etc_note = models.TextField(null=True)
    max_limit = models.BigIntegerField(null=True)
    dcls_month = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='options', null=True)  # Deposit와 연결 (1:N)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    intr_rate_type_nm = models.CharField(max_length=20, null=True, blank=True)
    save_trm = models.CharField(max_length=20)  # 기간

class Saving(models.Model):
    saving_code = models.CharField(max_length=50, unique=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    join_way = models.TextField(null=True)
    mtrt_int = models.TextField(null=True)
    spcl_cnd = models.TextField(null=True)
    join_deny = models.IntegerField()
    join_member = models.TextField()
    etc_note = models.TextField(null=True)
    max_limit = models.BigIntegerField(null=True)
    dcls_month = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name='options', null=True)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    intr_rate_type_nm = models.CharField(max_length=20, null=True, blank=True)
    save_trm = models.CharField(max_length=20)    
    
class Scrap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scraps')
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, null=True, blank=True)
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}의 스크랩: {self.deposit or self.saving}'