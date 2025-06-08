from rest_framework import serializers
from products.models import Deposit, Bank, Saving, DepositOption, SavingOption, Scrap

# 은행 직렬화
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name']

# 예금 옵션 직렬화
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'intr_rate_type_nm']

# 예금 상품 직렬화
class DepositSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    options = DepositOptionSerializer(many=True, read_only=True)  # ✅ related_name='options' 필요

    class Meta:
        model = Deposit
        fields = [
            'id', 'deposit_code', 'name', 'join_way',
            'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member',
            'etc_note', 'max_limit', 'dcls_month', 'bank', 'options'
        ]

# 적금 옵션 직렬화
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'intr_rate_type_nm']

# 적금 상품 직렬화
class SavingSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    options = SavingOptionSerializer(many=True, read_only=True)  # ✅ related_name='options' 필요

    class Meta:
        model = Saving
        fields = [
            'id', 'saving_code', 'name', 'join_way',
            'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member',
            'etc_note', 'max_limit', 'dcls_month', 'bank', 'options'
        ]

# 스크랩 직렬화
class ScrapSerializer(serializers.ModelSerializer):
    deposit = DepositSerializer(read_only=True)
    saving = SavingSerializer(read_only=True)
    deposit_id = serializers.IntegerField(write_only=True, required=False)
    saving_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Scrap
        fields = ['id', 'user', 'deposit', 'saving', 'deposit_id', 'saving_id']
        read_only_fields = ['user', 'deposit', 'saving']

    def create(self, validated_data):
        deposit_id = validated_data.pop('deposit_id', None)
        saving_id = validated_data.pop('saving_id', None)
        user = self.context['request'].user

        scrap = Scrap(user=user)
        if deposit_id:
            scrap.deposit_id = deposit_id
        if saving_id:
            scrap.saving_id = saving_id
        scrap.save()
        return scrap
