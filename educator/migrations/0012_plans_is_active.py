# Generated by Django 2.1.7 on 2019-03-31 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0011_user_referred_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active?'),
        ),
    ]
