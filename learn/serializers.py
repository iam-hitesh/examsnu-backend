from rest_framework import serializers
from .models import *
from educator.models import *

class LecturesWatchedSerializer(serializers.ModelSerializer):
    """
    Serializer for Lectures Views
    """
    class Meta(object):
        model = LecturesWatched
        fields = '__all__'
        read_only_fields = ('watched_at')

class HandoutsReadSerializer(serializers.ModelSerializer):
    """
    Serializer for Lectures Views
    """
    class Meta(object):
        model = HandoutsRead
        fields = '__all__'
        read_only_fields = ('read_at')

class OTSAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for Lectures Views
    """
    class Meta(object):
        model = OTSAttempt
        fields = '__all__'
        read_only_fields = ('started_at')

class OTSsubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Lectures Views
    """
    class Meta(object):
        model = OTSsubmission
        fields = '__all__'
        read_only_fields = ('submitted_at')

class QuizSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Lectures Views
    """
    class Meta(object):
        model = QuizSubmission
        fields = '__all__'
        read_only_fields = ('submitted_at')