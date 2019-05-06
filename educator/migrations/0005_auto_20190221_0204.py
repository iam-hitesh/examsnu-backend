# Generated by Django 2.1.4 on 2019-02-20 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0004_exams_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Notes/Handout Title')),
                ('handout_alt_title', models.CharField(default='', max_length=255, verbose_name='Handout Alternative Title(For users)')),
                ('description', models.TextField(default='', verbose_name='Notes/Handout description')),
                ('link', models.URLField(blank=True, verbose_name='Notes Link(If Any)')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='handout_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Handouts/Notes',
                'verbose_name_plural': 'Handouts/Notes',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title for Notes Lectures')),
                ('alt_title_notes', models.CharField(default='', max_length=255, verbose_name='Alternative Title(For users)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Notes Available for reading??')),
                ('active_on', models.DateTimeField(verbose_name='Notes will available for reading on??')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notes_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notes',
                'verbose_name_plural': 'Notes',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='OnlineExams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title)')),
                ('alt_title', models.CharField(default='', max_length=255, verbose_name='Alternative Title(For users)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Online Exam Available for users??')),
                ('active_on', models.DateTimeField(verbose_name='Online Exam will available on??')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ots_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Online Tests',
                'verbose_name_plural': 'Online Tests',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='QuestionOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_title', models.TextField(verbose_name='Option Title')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='option_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Options',
                'verbose_name_plural': 'Options',
                'ordering': ('option_title',),
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Question')),
                ('solution', models.TextField(verbose_name='Solution')),
                ('question_type', models.IntegerField(choices=[(1, 'Single Correct'), (2, 'Multiple Correct'), (3, 'Integer Type'), (4, 'Fill in the Blanks'), (5, 'True/False')], default=1, verbose_name='Question Type')),
                ('correct_marks', models.FloatField(default=0, verbose_name='Marks for Correct Answer')),
                ('negative_marks', models.FloatField(default=0, verbose_name='Negative Marking')),
                ('is_negative_marking', models.BooleanField(default=True, verbose_name='Is question have negative marking?')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('correct_options', models.ManyToManyField(related_name='correct_options', to='educator.QuestionOptions', verbose_name='Correct Option')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='question_created_by', to=settings.AUTH_USER_MODEL)),
                ('options', models.ManyToManyField(blank=True, related_name='given_options', to='educator.QuestionOptions', verbose_name='Given Choices')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('question',),
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title)')),
                ('alt_title', models.CharField(default='', max_length=255, verbose_name='Alternative Title(For users)')),
                ('duration', models.IntegerField(default=0, verbose_name='Test Duration')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Online Exam Available for users??')),
                ('active_on', models.DateTimeField(verbose_name='Online Exam will available on??')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ot_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Online Quiz',
                'verbose_name_plural': 'Online Quiz',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_title', models.CharField(default='', max_length=255, verbose_name='Topic title')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='topic_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Topic Name',
                'verbose_name_plural': 'Topics Name',
                'ordering': ('topic_title',),
            },
        ),
        migrations.CreateModel(
            name='VideoLectures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Title for Video Lectures')),
                ('alt_title_video', models.CharField(default='', max_length=255, verbose_name='Alternative Title(For users)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Video Lecture Live??')),
                ('active_on', models.DateTimeField(verbose_name='Video will available for watching on??')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video_lec_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Video Lecture',
                'verbose_name_plural': 'Video Lectures',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Video Title')),
                ('video_alt_title', models.CharField(default='', max_length=255, verbose_name='Video Alternative Title(For users)')),
                ('description', models.TextField(blank=True, default='', verbose_name='Video description')),
                ('link', models.URLField(verbose_name='Video Link')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Videos',
                'verbose_name_plural': 'Videos',
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='examcategory',
            name='alternative_name',
            field=models.CharField(default='', max_length=255, verbose_name='Category Alternative Name(For users)'),
        ),
        migrations.AddField(
            model_name='exams',
            name='alternative_name',
            field=models.CharField(default='', max_length=255, verbose_name='Exam Alternative Name(For users)'),
        ),
        migrations.AddField(
            model_name='plans',
            name='alternative_name',
            field=models.CharField(default='', max_length=255, verbose_name='Plan Alternative Name(For users)'),
        ),
        migrations.AddField(
            model_name='plans',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Plan description'),
        ),
        migrations.AddField(
            model_name='subjects',
            name='alternative_name',
            field=models.CharField(default='', max_length=255, verbose_name='Subject Alternative Name(For users)'),
        ),
        migrations.AddField(
            model_name='subjects',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Subject description'),
        ),
        migrations.AddField(
            model_name='videos',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Subjects', verbose_name='Suject video related to'),
        ),
        migrations.AddField(
            model_name='videos',
            name='topics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Topics', verbose_name='Topics video related to'),
        ),
        migrations.AddField(
            model_name='videolectures',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exam_related_to_videos', to='educator.Exams'),
        ),
        migrations.AddField(
            model_name='videolectures',
            name='videos',
            field=models.ManyToManyField(related_name='videos', to='educator.Videos', verbose_name='Videos'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='exam',
            field=models.ManyToManyField(to='educator.Exams', verbose_name='Exams related to Quiz'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(related_name='Questions', to='educator.Questions', verbose_name='Questions'),
        ),
        migrations.AddField(
            model_name='questions',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Subjects', verbose_name='Suject video related to'),
        ),
        migrations.AddField(
            model_name='questions',
            name='topics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Topics', verbose_name='Topics video related to'),
        ),
        migrations.AddField(
            model_name='onlineexams',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exam_related_to_test', to='educator.Exams', verbose_name='Exam related to Online Test'),
        ),
        migrations.AddField(
            model_name='onlineexams',
            name='questions',
            field=models.ManyToManyField(related_name='questions_for_ots', to='educator.Questions', verbose_name='Questions'),
        ),
        migrations.AddField(
            model_name='notes',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exam_related_to_notes', to='educator.Exams'),
        ),
        migrations.AddField(
            model_name='notes',
            name='notes',
            field=models.ManyToManyField(related_name='notes', to='educator.Handout', verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='handout',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Subjects', verbose_name='Suject video related to'),
        ),
        migrations.AddField(
            model_name='handout',
            name='topics',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.Topics', verbose_name='Topics video related to'),
        ),
    ]
