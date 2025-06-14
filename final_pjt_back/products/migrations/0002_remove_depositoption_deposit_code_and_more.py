# Generated by Django 4.2.16 on 2025-05-24 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositoption',
            name='deposit_code',
        ),
        migrations.RemoveField(
            model_name='savingoption',
            name='saving_code',
        ),
        migrations.AddField(
            model_name='depositoption',
            name='deposit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.deposit'),
        ),
        migrations.AddField(
            model_name='savingoption',
            name='saving',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='products.saving'),
        ),
    ]
