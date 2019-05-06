from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for All Kind Of Users
    """
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_educator': {'write_only': True},
            'access_level': {'write_only': True}
        }


class ExamCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Exam Category
    """
    created_by = serializers.SerializerMethodField()

    class Meta(object):
        model = ExamCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

class MinSubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Topics, It is minimal version for Topic Serializer, it give only title and id
    """
    class Meta(object):
        model = Subjects
        fields = ('id','subject_name',)
        read_only_fields = ('created_at', 'updated_at')

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Subjects
    """

    created_by = serializers.SerializerMethodField()

    class Meta(object):
        model = Subjects
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

class MinExamSerializer(serializers.ModelSerializer):
    """
    Serializer for Exams
    """

    class Meta(object):
        model = Exams
        fields = ('id','exam_name')
        read_only_fields = ('created_at', 'updated_at')

class ExamSerializer(serializers.ModelSerializer):
    """
    Serializer for Exam Category
    """

    created_by = serializers.SerializerMethodField()
    exam_category = serializers.SerializerMethodField()
    exam_category_id = serializers.SerializerMethodField()
    subjects = SubjectSerializer(read_only=True, many=True)

    class Meta(object):
        model = Exams
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_exam_category(self, instance):
        return instance.exam_category.category_name

    def get_exam_category_id(self,instance):
        return instance.exam_category.id

class MinTopicSerializer(serializers.ModelSerializer):
    """
    Serializer for Topics, It is minimal version for Topic Serializer, it give only title and id
    """
    class Meta(object):
        model = Topics
        fields = ('id','topic_title',)
        read_only_fields = ('created_at', 'updated_at')

class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer for Topics, It is full version, it will give all information regarding the specific topic
    """
    created_by = serializers.SerializerMethodField()

    class Meta(object):
        model = Topics
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

class PlanSerializer(serializers.ModelSerializer):
    """
    Serializer for Plans
    """
    created_by = serializers.SerializerMethodField()

    class Meta(object):
        model = Plans
        fields = '__all__'
        depth = 1
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment Details
    """
    plan = PlanSerializer(read_only=True, many=False)
    user = UserSerializer(read_only=True, many=False)
    created_by = UserSerializer(read_only=True, many=False)
    class Meta(object):
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class MinVideoSerializer(serializers.ModelSerializer):
    """
        Serializer for Video Lectures
    """

    class Meta(object):
        model = Videos
        fields = ('id','title','link')
        read_only_fields = ('created_at', 'updated_at')

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for Video Lectures
    """
    topics = MinTopicSerializer(read_only=True, many=True)
    subject = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()

    class Meta(object):
        model = Videos
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

    def get_subject(self, instance):
        return instance.subject.subject_name

    def get_subject_id(self, instance):
        return instance.subject.id

class MinHandoutSerializer(serializers.ModelSerializer):
    """
        Serializer for Video Lectures
    """

    class Meta(object):
        model = Videos
        fields = ('id','title','link')
        read_only_fields = ('created_at', 'updated_at')

class HandoutSerializer(serializers.ModelSerializer):
    """
    Serializer for Handouts
    """
    topics = MinTopicSerializer(read_only=True, many=True)
    subject = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()

    class Meta(object):
        model = Handout
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

    def get_subject(self, instance):
        return instance.subject.subject_name

    def get_subject_id(self, instance):
        return instance.subject.id

class MinQuestionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Topics, It is minimal version for Topic Serializer, it give only title and id
    """
    class Meta(object):
        model = QuestionOptions
        fields = ('id','option_title',)
        read_only_fields = ('created_at', 'updated_at')

class QuestionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question's -> Option's
    """
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()
    class Meta(object):
        model = QuestionOptions
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

class MinQuestionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Questions
        fields = ('id','question')
        read_only_fields = ('created_at', 'updated_at')

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question Bank
    """
    topics = MinTopicSerializer(read_only=True, many=True)
    subject = MinSubjectSerializer(read_only=True, many=False)
    options = MinQuestionOptionSerializer(read_only=True, many=True)
    correct_options = MinQuestionOptionSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()
    question_type = serializers.SerializerMethodField()
    question_type_id = serializers.SerializerMethodField()
    difficulty_level = serializers.SerializerMethodField()
    difficulty_level_id = serializers.SerializerMethodField()

    subject_name = serializers.SerializerMethodField()
    subject_name_id = serializers.SerializerMethodField()

    class Meta(object):
        model = Questions
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

    def get_question_type(self, instance):
        if instance.question_type == 1:
            return "Single Correct"
        elif instance.question_type == 2:
            return "Multiple Correct"
        elif instance.question_type == 3:
            return "Integer Type"
        elif instance.question_type == 4:
            return "Fill in the Blanks"
        else:
            return "True/False"

    def get_question_type_id(self, instance):
        return instance.question_type

    def get_difficulty_level(self, instance):
        if instance.difficulty_level == 1:
            return "Easy"
        elif instance.difficulty_level == 2:
            return "Medium"
        elif instance.difficulty_level == 3:
            return "Hard"
        elif instance.difficulty_level == 4:
            return "Expert"
        else:
            return "Easy"

    def get_difficulty_level_id(self, instance):
        return instance.difficulty_level

    def get_subject_name(self, instance):
        return instance.subject.subject_name

    def get_subject_name_id(self, instance):
        return instance.subject.id



class VideoLectureSerializer(serializers.ModelSerializer):
    """
    Video Lectures
    """
    exam = serializers.SerializerMethodField()
    exam_id = serializers.SerializerMethodField()
    videos = MinVideoSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()

    class Meta(object):
        model = VideoLectures
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

    def get_exam(self, instance):
        return instance.exam.exam_name

    def get_exam_id(self, instance):
        return instance.exam.id


class NoteSerializer(serializers.ModelSerializer):
    """
    Notes and Handout Serializer
    """
    subjects = MinSubjectSerializer(read_only=True, many=False)
    topics = MinTopicSerializer(read_only=True, many=True)
    exam = serializers.SerializerMethodField()
    exam_id = serializers.SerializerMethodField()
    notes = MinHandoutSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()

    class Meta(object):
        model = Notes
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

    def get_exam(self, instance):
        return instance.exam.exam_name

    def get_exam_id(self, instance):
        return instance.exam.id


class OnlineExamSerializer(serializers.ModelSerializer):
    """
    Online Exams
    """

    class Meta(object):
        model = OnlineExams
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class QuizSerializer(serializers.ModelSerializer):
    """
    Quizzes
    """
    questions = MinQuestionSerializer(read_only=True, many=True)

    class Meta(object):
        model = Quiz
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ExamQuizSerializer(serializers.ModelSerializer):
    """
    Quizzes
    """
    exam = MinExamSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField()
    created_by_id = serializers.SerializerMethodField()

    class Meta(object):
        model = Quiz
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_created_by(self, instance):
        return instance.created_by.name

    def get_created_by_id(self, instance):
        return instance.created_by.id

class RawQuizSerializer(serializers.ModelSerializer):
    """
    Quizzes
    """
    class Meta(object):
        model = Quiz
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')