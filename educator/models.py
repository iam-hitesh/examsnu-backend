from django.db import models
from django.contrib.auth.models import (
      AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
from django.conf import settings

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, name, password):
        user = self.model(email = email, name=name, password=password)
        user.set_password(password)
        user.is_educator = False
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email = email, name=name, password=password)
        user.is_active = True
        user.is_educator = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Here we are subclassing the Django AbstractBaseUser, which comes with only
    3 fields:
    1 - password
    2 - last_login
    3 - is_active
    Note than all fields would be required unless specified otherwise, with
    `required=False` in the parentheses.
    The PermissionsMixin is a model that helps you implement permission settings
    as-is or modified to your requirements.
    More info: https://goo.gl/YNL2ax
    """

    DEFAULT_LANG = ((1, 'English'),
                    (2, 'Hindi'))

    STAFF_ACCESS_LEVEL = ((1, 'SuperAdmin'),
                          (2, 'Admin'),
                          (3, 'Moderator'),
                          (4, 'Editor'),
                          (5, 'Content Writer'),
                          (6, 'Accounts'),
                          (7, 'Others'),
                          (8, 'Educator'),
                          (9, 'Student'))

    name = models.CharField(max_length=30, default='', verbose_name=u"Name of Educator")
    phone_number = models.CharField(max_length=15, default=0, unique=True, verbose_name=u"Mobile Number")
    email = models.EmailField(unique=True)
    unique_referral_code = models.CharField(max_length=12, editable=False, unique=True, default='', blank=True)
    referred_by = models.CharField(max_length=12, editable=True, default='', blank=True)
    profile_pic = models.ImageField(default='', blank=True, upload_to='static/users/profile_pic',
                                    verbose_name='Profile Picture')
    dob = models.DateField(default='1900-01-01', blank=True, null=True)
    location = models.CharField(max_length=50, default='', blank=True)
    education = models.CharField(max_length=255, default='', blank=True)
    default_lang = models.IntegerField(verbose_name="Default Lang for Exams", default=1, choices=DEFAULT_LANG)

    is_educator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    access_level = models.IntegerField(verbose_name='Access level', default=7, choices=STAFF_ACCESS_LEVEL)
    is_active = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.name

    def natural_key(self):
        return self.email

    def __str__(self):
        return "{} - {}".format(self.name, self.email)

    class Meta:
        ordering = ('email',)
        verbose_name = 'User profile'
        verbose_name_plural = 'User Profile'



class ExamCategory(models.Model):
    category_name = models.CharField(max_length=255, verbose_name=u"Exam Category Name", blank=False, default='')
    alternative_name = models.CharField(max_length=255, verbose_name=u"Category Alternative Name(For users)",
                                        blank=False, default='')
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='category_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ('category_name',)
        verbose_name = "Category Name"
        verbose_name_plural = "Categries Name"

class Subjects(models.Model):
    subject_name = models.CharField(max_length=255, verbose_name=u"Subject Name", blank=False, default='')
    alternative_name = models.CharField(max_length=255, verbose_name=u"Subject Alternative Name(For users)", blank=False, default='')
    description = models.TextField(verbose_name=u'Subject description', blank=True, default='')
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='subject_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ('subject_name',)
        verbose_name = "Subject Name"
        verbose_name_plural = "Subjects Name"

class Topics(models.Model):
    topic_title = models.CharField(max_length=255, verbose_name=u"Topic title", blank=False, default='')
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='topic_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.topic_title

    class Meta:
        ordering = ('topic_title',)
        verbose_name = "Topic Name"
        verbose_name_plural = "Topics Name"

class Exams(models.Model):
    exam_name = models.CharField(max_length=255, verbose_name=u"Exam Name", blank=False, default='')
    alternative_name = models.CharField(max_length=255, verbose_name=u"Exam Alternative Name(For users)",
                                        blank=False, default='')
    subjects = models.ManyToManyField(Subjects, blank=True)
    exam_category = models.ForeignKey(ExamCategory, related_name="exam_category", on_delete=models.CASCADE, default=1)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='exam_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.exam_name

    class Meta:
        ordering = ('exam_name',)
        verbose_name = "Exam Name"
        verbose_name_plural = "Exams Name"

class Plans(models.Model):
    plan_name = models.CharField(max_length=255, verbose_name=u"Plan Name", blank=False, default='')
    alternative_name = models.CharField(max_length=255, verbose_name=u"Plan Alternative Name(For users)",
                                        blank=False, default='')
    price = models.FloatField(verbose_name=u"Price of the Plan", default=0.0)
    description = models.TextField(verbose_name=u'Plan description', blank=True, default='')
    exams = models.ManyToManyField(Exams, blank=True)
    validity = models.IntegerField(default=90, verbose_name=u"Plan Validity(In Days)")
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    is_active = models.BooleanField(verbose_name=u"is active?", default=True)
    created_by = models.ForeignKey(User, related_name='plan_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.exam_name

    class Meta:
        ordering = ('plan_name',)
        verbose_name = "Plan Name"
        verbose_name_plural = "Plan Name"

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, related_name="Plans", on_delete=models.CASCADE)
    payment_for = models.CharField(verbose_name=u"Payment done for", max_length=120, null=False, blank=False, default='')
    payment_amount = models.FloatField(verbose_name=u"Payment amount", default=0)
    payment_id = models.CharField(verbose_name="Payment ID", max_length=120, default='')
    payment_gateway = models.CharField(verbose_name="Payment gateway", max_length=120, default='')
    payment_status = models.CharField(verbose_name="Payment status", max_length=120, default='')
    bank_ref_num = models.CharField(verbose_name="Payment Bank Ref. Number", max_length=120, default='')
    pg_type = models.CharField(verbose_name="Payment PG Type", max_length=120, default='')
    pay_mode = models.CharField(verbose_name="Payment Mode", max_length=120, default='')
    paid_on = models.DateTimeField(verbose_name="Payment done on", default=timezone.now)
    expire_on = models.DateTimeField(verbose_name="Plan will expire on", default=timezone.now)
    verification_code = models.CharField(verbose_name="Any Verification code", max_length=120, default='')

    def __str__(self):
        return self.payment_for

    class Meta:
        ordering = ('payment_id',)
        verbose_name = 'Payment Details'
        verbose_name_plural = 'Payment Details'


class Videos(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Video Title", default='')
    video_alt_title = models.CharField(max_length=255, verbose_name=u"Video Alternative Title(For users)",
                                        blank=False, default='')
    description = models.TextField(verbose_name=u'Video description', blank=True, default='')
    link = models.URLField(verbose_name=u"Video Link", blank=False)
    subject = models.ForeignKey(Subjects, verbose_name=u"Suject video related to",on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topics, verbose_name=u"Topics video related to")
    created_by = models.ForeignKey(User, related_name='video_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Videos'
        verbose_name_plural = 'Videos'

class Handout(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Notes/Handout Title", default='')
    handout_alt_title = models.CharField(max_length=255, verbose_name=u"Handout Alternative Title(For users)",
                                 blank=False, default='')
    description = models.TextField(verbose_name=u'Notes/Handout description', blank=False, default='')
    link = models.URLField(verbose_name=u"Notes Link(If Any)", blank=True)
    subject = models.ForeignKey(Subjects, verbose_name=u"Suject video related to", on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topics, verbose_name=u"Topics video related to")
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='handout_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Handouts/Notes'
        verbose_name_plural = 'Handouts/Notes'

class QuestionOptions(models.Model):
    option_title = models.TextField(verbose_name=u"Option Title", blank=False)
    hindi_option_title = models.TextField(verbose_name=u"Hindi Title", blank=False)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)
    created_by = models.ForeignKey(User, related_name='option_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)

    def __str__(self):
        return self.option_title

    class Meta:
        ordering = ('option_title',)
        verbose_name = 'Options'
        verbose_name_plural = 'Options'

class Questions(models.Model):
    QUESTION_TYPE = ((1, 'Single Correct'),
                (2, 'Multiple Correct'),
                (3, 'Integer Type'),
                (4, 'Fill in the Blanks'),
                (5, 'True/False'),
                )

    DIFFICULTY_LEVEL = ((1,'Easy'),(2,'Medium'),(3,'Hard'),(4,'Expert'))


    question = models.TextField(verbose_name=u"Question", blank=False)
    hindi_question = models.TextField(verbose_name=u"Question in Hindi", blank=False)
    solution = models.TextField(verbose_name=u"Solution", blank=False)
    hindi_solution = models.TextField(verbose_name=u"Solution in Hindi", blank=False)
    subject = models.ForeignKey(Subjects, verbose_name=u"Suject video related to", on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topics, verbose_name=u"Topics video related to")
    question_type = models.IntegerField(verbose_name=u"Question Type", default=1, choices=QUESTION_TYPE, blank=False)
    difficulty_level = models.IntegerField(verbose_name=u"Question Difficulty Level", default=1, choices=DIFFICULTY_LEVEL, blank=False)
    options = models.ManyToManyField(QuestionOptions, related_name="given_options", verbose_name=u"Given Choices", blank=True)
    correct_options = models.ManyToManyField(QuestionOptions, related_name="correct_options",verbose_name=u"Correct Option", blank=False)
    correct_marks = models.FloatField(verbose_name=u"Marks for Correct Answer", default=0)
    negative_marks = models.FloatField(verbose_name=u"Negative Marking", default=0)
    is_negative_marking = models.BooleanField(verbose_name=u"Is question have negative marking?", default=True)
    avg_time = models.IntegerField(verbose_name=u"Average Solving Time(in seconds)", default=10)
    created_by = models.ForeignKey(User, related_name='question_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('question',)
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


# Part 2 of the Educator Section

class VideoLectures(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Title for Video Lectures", blank=False, default='')
    alt_title_video = models.CharField(max_length=255, verbose_name=u"Alternative Title(For users)",
                                 blank=False, default='')
    exam = models.ForeignKey(Exams, related_name='exam_related_to_videos', blank=False, on_delete=models.CASCADE, default=1)
    videos = models.ManyToManyField(Videos, related_name="videos", verbose_name=u"Videos", blank=False)
    is_active = models.BooleanField(verbose_name=u"Is Video Lecture Live??", default=False)
    active_on = models.DateTimeField(verbose_name=u"Video will available for watching on??")
    created_by = models.ForeignKey(User, related_name='video_lec_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Video Lecture'
        verbose_name_plural = 'Video Lectures'

class Notes(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Title for Notes Lectures", blank=False, default='')
    alt_title_notes = models.CharField(max_length=255, verbose_name=u"Alternative Title(For users)",
                                 blank=False, default='')
    exam = models.ForeignKey(Exams, related_name='exam_related_to_notes', blank=False, on_delete=models.CASCADE, default=1)
    notes = models.ManyToManyField(Handout, related_name="notes", verbose_name=u"Notes", blank=False)
    is_active = models.BooleanField(verbose_name=u"Is Notes Available for reading??", default=False)
    active_on = models.DateTimeField(verbose_name=u"Notes will available for reading on??")
    created_by = models.ForeignKey(User, related_name='notes_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'


class OnlineExams(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Title)",
                                 blank=False, default='')
    alt_title = models.CharField(max_length=255, verbose_name=u"Alternative Title(For users)",
                                 blank=False, default='')
    exam = models.ForeignKey(Exams, related_name='exam_related_to_test', on_delete=models.CASCADE, blank=False, default=1, verbose_name=u"Exam related to Online Test")
    questions = models.ManyToManyField(Questions, related_name="questions_for_ots", verbose_name="Questions", blank=False)
    subjects = models.ManyToManyField(Subjects, related_name="subjects_related_to_ots", verbose_name="Subjects",
                                       blank=False)
    is_active = models.BooleanField(verbose_name=u"Is Online Exam Available for users??", default=False)
    is_free = models.BooleanField(verbose_name=u"Is Online Exam is Available Freely??", default=False)
    active_on = models.DateTimeField(verbose_name=u"Online Exam will available on??")
    expire_on = models.DateTimeField(verbose_name=u"Online Exam Will expire on??",default='2020-01-01 23:55:55')
    created_by = models.ForeignKey(User, related_name='ots_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Online Tests'
        verbose_name_plural = 'Online Tests'


class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Title)",
                             blank=False, default='')
    alt_title = models.CharField(max_length=255, verbose_name=u"Alternative Title(For users)",
                                 blank=False, default='')
    duration = models.IntegerField(verbose_name=u"Test Duration(In Minutes)", blank=False, default=0)
    exam = models.ManyToManyField(Exams, blank=False, verbose_name=u"Exams related to Quiz")
    questions = models.ManyToManyField(Questions, related_name="Questions", verbose_name="Questions", blank=False)
    is_active = models.BooleanField(verbose_name=u"Is Online Exam Available for users??", default=False)
    active_on = models.DateTimeField(verbose_name=u"Online Exam will available on??")
    expire_on = models.DateTimeField(verbose_name=u"Online Quiz Will expire on??",default='2020-01-01 23:55:55')
    created_by = models.ForeignKey(User, related_name='ot_created_by', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name=u"Created At", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=u"Updated At", auto_now=True)
    is_deleted = models.BooleanField(verbose_name=u"is deleted?", default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Online Quiz'
        verbose_name_plural = 'Online Quiz'
