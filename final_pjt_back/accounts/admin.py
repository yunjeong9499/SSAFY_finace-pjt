

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': (
                'name', 
                'nickname', 
                'profile_image',
                'age_group',
                'job',
                'income_level',
                'consumption_type',
                'saving_goal',
                'saving_period',
                'monthly_saving_amount',
                'preference_tags',
                'survey_completed',
            )
        }),
    )
