from django.db import models
from educator.models import *
from django.utils import timezone


class LecturesWatched(models.Model):
    watched_by =  models.ForeignKey(User, related_name='lecture_watched_by', on_delete=models.CASCADE, blank=False)
    video_id = models.ForeignKey(Videos, verbose_name=u"Video Related to", on_delete=models.CASCADE, blank=False)
    lect_id = models.ForeignKey(VideoLectures, verbose_name=u"Video Lecture ID", on_delete=models.CASCADE, blank=False)
    exam_id = models.ForeignKey(Exams, verbose_name=u"Exam ID", on_delete=models.CASCADE, blank=False)
    watched_at = models.DateTimeField(verbose_name=u"Watched At", default=timezone.now)

    def __str__(self):
        return "Watched"

    class Meta:
        ordering = ('watched_at',)
        verbose_name = 'Lecture Views'
        verbose_name_plural = 'Lectures Views'


class HandoutsRead(models.Model):
    read_by =  models.ForeignKey(User, related_name='handout_read_by', on_delete=models.CASCADE, blank=False)
    handout_id = models.ForeignKey(Handout, verbose_name=u"Handout ID", on_delete=models.CASCADE, blank=False)
    notes_id = models.ForeignKey(Notes, verbose_name=u"Notes ID", on_delete=models.CASCADE, blank=False)
    exam_id = models.ForeignKey(Exams, verbose_name=u"Exam ID", on_delete=models.CASCADE, blank=False)
    read_at = models.DateTimeField(verbose_name=u"Read At", default=timezone.now)

    def __str__(self):
        return "Read"

    class Meta:
        ordering = ('read_at',)
        verbose_name = 'Handout Reads'
        verbose_name_plural = 'Handout Reads'

class OTSAttempt(models.Model):
    attempt_by = models.ForeignKey(User, related_name='test_attempted_by', on_delete=models.CASCADE, blank=False)
    ots_id = models.ForeignKey(OnlineExams, related_name="ots_id", on_delete=models.CASCADE, blank=False)
    exam_id = models.ForeignKey(Exams, verbose_name=u"Exam ID", on_delete=models.CASCADE, blank=False)
    total_marks = models.FloatField(default=0.0)
    correct_marks = models.FloatField(default=0.0)
    negative_marks = models.FloatField(default=0.0)
    started_at = models.DateTimeField(verbose_name=u"Exam started At", default=timezone.now)

    def __str__(self):
        return "Started"

    class Meta:
        ordering = ('started_at',)
        verbose_name = 'OTS Attempt'
        verbose_name_plural = 'OTS Attempt'


class OTSsubmission(models.Model):
    attempt_by = models.ForeignKey(User, related_name='ots_attempted_by', on_delete=models.CASCADE, blank=False)
    ots_id = models.ForeignKey(OnlineExams, related_name="otsattempt_ots_id", on_delete=models.CASCADE, blank=False)
    exam_id = models.ForeignKey(Exams, verbose_name=u"Exam ID", on_delete=models.CASCADE, blank=False)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    is_correct = models.BooleanField(default=False)
    marks_get = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(verbose_name=u"Submitted at", default=timezone.now)

    def __str__(self):
        return "Submitted"

    class Meta:
        ordering = ('submitted_at',)
        verbose_name = 'OTS Submissions'
        verbose_name_plural = 'OTS Submissions'


class QuizSubmission(models.Model):
    attempt_by = models.ForeignKey(User, related_name='quiz_attempted_by', on_delete=models.CASCADE, blank=False)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(verbose_name=u"Submitted at", default=timezone.now)

    def __str__(self):
        return "Submitted"

    class Meta:
        ordering = ('submitted_at',)
        verbose_name = 'Quiz Submissions'
        verbose_name_plural = 'Quiz Submissions'


