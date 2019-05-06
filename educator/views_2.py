from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY
)
from rest_framework.response import Response
from django.http import JsonResponse
from .backends import AuthBackend
import json

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from .models import *
from .serializers import *
from .pagination import *



class VideoLectureView(APIView):
    """
    Payment View

    METHOD GET - FOR GETTING ALL VIDEO LECTURE
    METHOD POST - FOR ADDING A VIDEO LECTURE
    METHOD PUT - FOR UPDATING A VIDEO LECTURE
    """

    def get(self, request):
        page = request.GET.get('page')
        try:
            limit = 100 * int(page)
            offset = 100 * int(int(page) - 1)

            video_lec = VideoLectures.objects.all()[offset:limit]
            video_lec_data = VideoLectureSerializer(video_lec, many=True)

            return Response(video_lec_data.data, status=HTTP_200_OK)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


    def post(self, request):
        data = json.loads(request.body)
        try:
            title = data['title']
            alt_title_video = data['alt_title_video']
            exam_id = data['exam']
            is_active = data['is_active']
            active_on = data['active_on']

            if is_active == 'true':
                is_active = True
            else:
                is_active = False

            exam = Exams.objects.get(id=exam_id)

            video_lec = VideoLectures.objects.create(
                title = title,
                alt_title_video = alt_title_video,
                exam = exam,
                is_active = is_active,
                active_on = active_on,
                created_by = request.user,
                is_deleted = False,
            )

            if video_lec:
                return JsonResponse({'status': 1, 'message': 'Video Lecture added', 'id': video_lec.id},
                                    status=HTTP_201_CREATED)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


    def put(self, request):
        data = json.loads(request.body)
        try:
            video_lecture_id = data['video_lecture_id']
            title = data['title']
            alt_title_video = data['alt_title_video']
            exam_id = data['exam']
            is_active = data['is_active']
            active_on = data['active_on']
            is_deleted = data['is_deleted']

            if is_active == 'true':
                is_active = True
            else:
                is_active = False

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            exam = Exams.objects.get(id=exam_id)

            video_lec = VideoLectures.objects.filter(id=video_lecture_id).update(
                title=title,
                alt_title_video=alt_title_video,
                exam=exam,
                is_active=is_active,
                active_on=active_on,
                created_by=request.user,
                is_deleted=is_deleted,
            )

            if video_lec:
                video_lec = VideoLectures.objects.get(id=video_lecture_id)
                video_lec_data = VideoLectureSerializer(video_lec, many=False)

                return Response(video_lec_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleVideoLecView(APIView):
    """
    This is for getting a Video Lecture
    """

    def get(self, request):
        id = request.GET.get('id')
        try:
            video_lec = VideoLectures.objects.get(id=id)
            video_lec_data = VideoLectureSerializer(video_lec, many=False)

            return Response(video_lec_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)

        try:
            lecture_id = data['lecture_id']
            video_id = data['video_id']

            lecture = VideoLectures.objects.get(id=lecture_id)
            lecture_data = VideoLectureSerializer(lecture, many=False)

            if lecture:
                lecture.videos.add(video_id)

                return Response(lecture_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads(request.body)

        try:
            lecture_id = data['lecture_id']
            video_id = data['video_id']

            lecture = VideoLectures.objects.get(id=lecture_id)
            lecture_data = VideoLectureSerializer(lecture, many=False)

            if lecture:
                lecture.videos.remove(video_id)

                return Response(lecture_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)




class SearchVideoLecView(generics.ListAPIView):
    """
    This view for searching Video Lecture in the Database
    """
    queryset = VideoLectures.objects.all().order_by('-id')
    serializer_class = VideoLectureSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'title',
        'alt_title_video',
        'exam__exam_name',
        'is_active',
        'created_by__name',
        'created_at'
    )


class NotesView(APIView):
    """
    Payment View

    METHOD GET - FOR GETTING ALL VIDEO LECTURE
    METHOD POST - FOR ADDING A VIDEO LECTURE
    METHOD PUT - FOR UPDATING A VIDEO LECTURE
    """

    def get(self, request):
        page = request.GET.get('page')
        try:
            limit = 100 * int(page)
            offset = 100 * int(int(page) - 1)

            notes = Notes.objects.all()[offset:limit]
            notes_data = NoteSerializer(notes, many=True)

            return Response(notes_data.data, status=HTTP_200_OK)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            data = json.loads(request.body)
            title = data['title']
            alt_title_notes = data['alt_title_notes']
            exam_id = data['exam']
            is_active = data['is_active']
            active_on = data['active_on']

            if is_active == 'true':
                is_active = True
            else:
                is_active = False

            exam = Exams.objects.get(id=exam_id)

            notes_insert = Notes.objects.create(
                title=title,
                alt_title_notes=alt_title_notes,
                exam=exam,
                is_active=is_active,
                active_on=active_on,
                created_by=request.user,
                is_deleted=False,
            )

            if notes_insert:
                return JsonResponse({'status': 1, 'message': 'added', 'id': notes_insert.id},
                                    status=HTTP_201_CREATED)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


    def put(self, request):
        data = json.loads(request.body)
        try:
            notes_lecture_id = data['notes_lecture_id']
            title = data['title']
            alt_title_notes = data['alt_title_notes']
            exam_id = data['exam']
            is_active = data['is_active']
            active_on = data['active_on']
            is_deleted = data['is_deleted']

            if is_active == 'true':
                is_active = True
            else:
                is_active = False

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            exam = Exams.objects.get(id=exam_id)

            notes_update = Notes.objects.filter(id=notes_lecture_id).update(
                title=title,
                alt_title_notes=alt_title_notes,
                exam=exam,
                is_active=is_active,
                active_on=active_on,
                created_by=request.user,
                is_deleted=is_deleted,
            )

            if notes_update:
                return JsonResponse({'status': 1, 'message': 'updated'},
                                    status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleNotesView(APIView):
    """
    This is for getting a Video Lecture
    """

    def get(self, request):
        id = request.GET.get('id')
        try:
            notes_lec = Notes.objects.get(id=id)
            notes_lec_data = NoteSerializer(notes_lec, many=False)

            return Response(notes_lec_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)

        try:
            handout_id = data['handout_id']
            note_id = data['note_id']

            notes = Notes.objects.get(id=note_id)
            notes_data = NoteSerializer(notes, many=False)

            if notes:
                notes.notes.add(handout_id)

                return Response(notes_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads(request.body)

        try:
            handout_id = data['handout_id']
            note_id = data['note_id']

            notes = Notes.objects.get(id=note_id)
            notes_data = NoteSerializer(notes, many=False)

            if notes:
                notes.notes.remove(handout_id)

                return Response(notes_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

class SearchNotesView(generics.ListAPIView):
    """
    This view for searching Notes in the Database
    """
    queryset = Notes.objects.all().order_by('-id')
    serializer_class = NoteSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'title',
        'alt_title_notes',
        'exam__exam_name',
        'is_active',
        'created_by__name',
        'created_at'
    )


# Views for Creating Quizzes

class QuizzesView(APIView):
    """
    Quizzes View

    METHOD GET - FOR GETTING ALL Quizzes
    METHOD POST - FOR ADDING A Quiz
    METHOD PUT - FOR UPDATING A Quiz
    """

    def get(self, request):
        page = request.GET.get('page')
        try:
            limit = 100 * int(page)
            offset = 100 * int(int(page) - 1)

            quiz = Quiz.objects.all()[offset:limit]
            quizzes_data = ExamQuizSerializer(quiz, many=True)

            return Response(quizzes_data.data, status=HTTP_200_OK)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        title = data['title']
        alt_title = data['alt_title']
        duration = data['duration']
        exam_id = data['exam']
        is_active = data['is_active']
        active_on = data['active_on']
        expire_on = data['expire_on']

        if is_active == 'true':
            is_active = True
        else:
            is_active = False

        quiz_insert = Quiz.objects.create(
            title=title,
            alt_title=alt_title,
            duration=duration,
            is_active=is_active,
            active_on=active_on,
            expire_on=expire_on,
            created_by=request.user,
            is_deleted=False,
        )

        if quiz_insert:
            for exam in exam_id:
                quiz_insert.exam.add(exam)

            return JsonResponse({'status': 1, 'message': 'added', 'id': quiz_insert.id},
                                status=HTTP_201_CREATED)
        else:
            return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)


    def put(self, request):
        data = json.loads(request.body)
        try:
            quiz_id = data['quiz_id']
            title = data['title']
            alt_title = data['alt_title']
            duration = data['duration']
            is_active = data['is_active']
            active_on = data['active_on']
            expire_on = data['expire_on']
            is_deleted = data['is_deleted']

            if is_active == 'true':
                is_active = True
            else:
                is_active = False

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            update_exam = data['exam']

            quiz_update = Quiz.objects.filter(id=quiz_id).update(
                title=title,
                alt_title=alt_title,
                duration=duration,
                is_active=is_active,
                active_on=active_on,
                expire_on=expire_on,
                created_by=request.user,
                is_deleted=is_deleted,
            )

            if quiz_update:
                quiz_update_exam = Quiz.objects.get(id=quiz_id)
                all_exams = Exams.objects.all()

                for exam in all_exams:
                    exam_id = exam.id
                    quiz_update_exam.exam.remove(exam_id)

                for exam in update_exam:
                    quiz_update_exam.exam.add(exam)

                return JsonResponse({'status': 1, 'message': 'updated'},
                                    status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleQuizView(APIView):
    """
    This is for getting a Quiz
    """

    def get(self, request):
        id = request.GET.get('id')
        try:
            quiz = Quiz.objects.get(id=id)
            quiz_data = RawQuizSerializer(quiz, many=False)

            return Response(quiz_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)

        try:
            quiz_id = data['quiz_id']
            question_id = data['question_id']

            quiz = Quiz.objects.get(id=quiz_id)
            quiz_data = QuizSerializer(quiz, many=False)

            if quiz:
                quiz.questions.add(question_id)

                return Response(quiz_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads(request.body)

        try:
            quiz_id = data['quiz_id']
            question_id = data['question_id']

            quiz = Quiz.objects.get(id=quiz_id)
            quiz_data = QuizSerializer(quiz, many=False)

            if quiz:
                quiz.questions.remove(question_id)

                return Response(quiz_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

class SearchQuizView(generics.ListAPIView):
    """
    This view for searching Quiz in database
    """
    queryset = Quiz.objects.all().order_by('-id')
    serializer_class = ExamQuizSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'title',
        'alt_title',
        'exam__exam_name',
        'is_active',
        'created_by__name',
        'created_at'
    )


