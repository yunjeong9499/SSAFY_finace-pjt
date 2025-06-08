# from django.apps import AppConfig


# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'

#     def ready(self):
#         from . import serializers

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        print("✅ accounts.apps.AccountsConfig.ready() called")
        from . import serializers  # ✅ 강제 로딩
