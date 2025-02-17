# Generated by Django 2.1.4 on 2019-02-20 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0002_auto_20190220_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(default='', max_length=255, verbose_name='Subject Name')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subject_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subject Name',
                'verbose_name_plural': 'Subjects Name',
                'ordering': ('subject_name',),
            },
        ),
    ]
