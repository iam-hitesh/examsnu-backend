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
from django.db.models import Q
from .serializers import *
from .pagination import *

# Login API
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):

    # Get data into JSON Format
    data = json.loads(request.body.decode("utf-8"))

    # Email or Username
    email = data['email']
    password = data['password']


    if email is None or password is None:
        return Response({'status': 0, 'error': 'Please provide both Email/Mobile Number and password'}, status=HTTP_400_BAD_REQUEST)


    # Call authbackend class from backends.py file for custom authentication
    Auth = AuthBackend()
    user = Auth.authenticate(email=email, password=password, is_staff = 1, is_active = 1)

    if not user:
        return Response({'status':0, 'error': 'Invalid Credentials'}, status=HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)

    user = User.objects.get(id=user.id)
    serializer = UserSerializer(user, many=False)

    return Response({'status':1, 'token': token.key, 'profile':serializer.data}, status=HTTP_200_OK)


class Profile(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id = request.user.id, email = request.user.email)
            serializer = UserSerializer(user, many=False)

            return Response(serializer.data, status=HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({'status':0, 'message': 'No User details found'}, status = HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status':0, 'message': 'Some Error Occurred'}, status = HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
     Logout by deleting the authentication token from Database
    """

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'status': 1, 'message': 'Logged Out'}, status=HTTP_200_OK)


# OTHER FUNCTIONALITIES
class ExamCategoryView(APIView):
    """
    Exam Categories
    
    METHOD GET - FOR GETTING ALL EXAM CATEGORY
    METHOD POST - FOR CREATING A EXAM CATEGORY
    METHOD PUT - FOR UPDATING A EXAM CATEGORY
    """
    def get(self, request):
        try:
            if request.user.is_superuser:
                category = ExamCategory.objects.all()
                category_data = ExamCategorySerializer(category, many=True)

                return Response(category_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status':0,'message':'You are not authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status':0,'message':'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                category_name = data['category_name']
                alternative_name = data['alternative_name']

                category = ExamCategory.objects.create(
                    category_name = category_name,
                    alternative_name = alternative_name,
                    is_deleted = False,
                    created_by = request.user
                )

                if category:
                    category = ExamCategory.objects.all()
                    category_data = ExamCategorySerializer(category, many=True)

                    return Response(category_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status':0, 'message':'Could not created'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status':0, 'message':'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        """
        This is method is for updating the data and used for setting status is_deleted to True/False
        
        
        :param request: is_deleted
        :return: updated_categories
        """
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                category_id = data['category_id']
                category_name = data['category_name']
                alternative_name = data['alternative_name']
                is_deleted = data['is_deleted']

                if is_deleted == 'true':
                    is_deleted = True
                else:
                    is_deleted = False

                category = ExamCategory.objects.filter(id=category_id).update(
                    category_name=category_name,
                    alternative_name=alternative_name,
                    is_deleted=is_deleted,
                )

                if category:
                    category = ExamCategory.objects.all()
                    category_data = ExamCategorySerializer(category, many=True)

                    return Response(category_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleExamCategoryView(APIView):
    """
    This is for gettting Single Category
    """
    def get(self, request):

        id = request.GET.get('id')

        try:
            if request.user.is_superuser:
                category = ExamCategory.objects.get(id=id)
                category_data = ExamCategorySerializer(category, many=False)

                return Response(category_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SubjectsView(APIView):
    """
    Exam Categories

    METHOD GET - FOR GETTING ALL SUBJECTS
    METHOD POST - FOR ADDING A SUBJECT
    METHOD PUT - FOR UPDATING A SUBJECT
    """

    def get(self, request):
        try:
            if request.user.is_superuser:
                subjects = Subjects.objects.all()
                subjects_data = SubjectSerializer(subjects, many=True)

                return Response(subjects_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'You are not authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                subject_name = data['subject_name']
                alternative_name = data['alternative_name']
                description = data['description']

                subject = Subjects.objects.create(
                    subject_name=subject_name,
                    alternative_name=alternative_name,
                    description=description,
                    is_deleted=False,
                    created_by=request.user
                )

                if subject:
                    subjects = Subjects.objects.all()
                    subjects_data = SubjectSerializer(subjects, many=True)

                    return Response(subjects_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        """
        This is method is for updating the data and used for setting status is_deleted to True/False
        :param request: subject_id
        :return: list of updated data
        """
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                subject_id = data['subject_id']
                subject_name = data['subject_name']
                alternative_name = data['alternative_name']
                description = data['description'],
                is_deleted = data['is_deleted']

                if is_deleted == 'true':
                    is_deleted = True
                else:
                    is_deleted = False

                category = Subjects.objects.filter(id=subject_id).update(
                    subject_name=subject_name,
                    alternative_name=alternative_name,
                    description = description,
                    is_deleted = is_deleted,
                )

                if category:
                    subjects = Subjects.objects.all()
                    subjects_data = SubjectSerializer(subjects, many=True)

                    return Response(subjects_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SingleSubjectView(APIView):
    """
    This is for gettting Single Subject
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            if request.user.is_superuser:
                subject = Subjects.objects.get(id=id)
                subject_data = SubjectSerializer(subject, many=False)

                return Response(subject_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class TopicsView(APIView):
    """
    Exam Categories

    METHOD GET - FOR GETTING ALL TOPICS
    METHOD POST - FOR ADDING A TOPIC
    METHOD PUT - FOR UPDATING A TOPIC
    """

    def get(self, request):
        try:
            topics = Topics.objects.all()
            topics_data = TopicSerializer(topics, many=True)

            return Response(topics_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            topic_title = data['topic_title']

            topic = Topics.objects.create(
                topic_title=topic_title,
                is_deleted=False,
                created_by=request.user
            )

            if topic:
                topics = Topics.objects.all()
                topics_data = TopicSerializer(topics, many=True)

                return Response(topics_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        """
        This is method is for updating the data and used for setting status is_deleted to True/False
        :param request: subject_id
        :return: list of updated data
        """
        data = json.loads(request.body)
        try:
            topic_id = data['topic_id']
            topic_title = data['topic_title']
            is_deleted = data['is_deleted']

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            topic = Topics.objects.filter(id=topic_id).update(
                topic_title=topic_title,
                is_deleted=is_deleted,
            )

            if topic:
                topics = Topics.objects.all()
                topics_data = TopicSerializer(topics, many=True)

                return Response(topics_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SingleTopicView(APIView):
    """
    This is for gettting Single Topic
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            topic = Topics.objects.get(id=id)
            topic_data = TopicSerializer(topic, many=False)

            return Response(topic_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)



class ExamsView(APIView):
    """
    Exams

    METHOD GET - FOR GETTING ALL EXAMS 
    METHOD POST - FOR ADDING A EXAM
    METHOD PUT - FOR UPDATING A EXAM
    """

    def get(self, request):
        try:
            if request.user.is_superuser:
                exams = Exams.objects.all().order_by('exam_name')
                exams_data = ExamSerializer(exams, many=True)

                return Response(exams_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'You are not authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                exam_name = data['exam_name']
                alternative_name = data['alternative_name']
                exam_category = data['exam_category']

                exam_category = ExamCategory.objects.get(id=exam_category)

                subject_list = data['subject_list']

                exam = Exams.objects.create(
                    exam_name=exam_name,
                    alternative_name=alternative_name,
                    exam_category=exam_category,
                    is_deleted=False,
                    created_by=request.user
                )

                if exam:
                    for subject_id in subject_list:
                        exam.subjects.add(subject_id)

                    exams = Exams.objects.all().order_by('exam_name')
                    exams_data = ExamSerializer(exams, many=True)

                    return Response(exams_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        """
        Currently this method is being used for deleting the exam only means setting is_deleted=True
        :param request: 
        :return: 
        """
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                exam_id = data['exam_id']
                exam_name = data['exam_name']
                alternative_name = data['alternative_name']
                exam_category = data['exam_category']
                is_deleted = data['is_deleted']

                if is_deleted == 'true':
                    is_deleted = True
                else:
                    is_deleted = False

                new_subject_list = data['subjects']
                # new_subjects = subject_list.split(",")

                exam = Exams.objects.filter(id=exam_id).update(
                    exam_name=exam_name,
                    alternative_name=alternative_name,
                    exam_category=exam_category,
                    is_deleted=is_deleted,
                )

                if exam:
                    exam_update = Exams.objects.get(id=exam_id)
                    all_subjects = Subjects.objects.all()

                    for subject in all_subjects:
                        subject_id = subject.id
                        exam_update.subjects.remove(subject_id)

                    for subject_id in new_subject_list:
                        exam_update.subjects.add(subject_id)

                    exams = Exams.objects.all().order_by('exam_name')
                    exams_data = ExamSerializer(exams, many=True)

                    return Response(exams_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SingleExamView(APIView):
    """
    This is for getting Single Exam Details
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            if request.user.is_superuser:
                exam = Exams.objects.get(id=id)
                exam_data = ExamSerializer(exam, many=False)

                return Response(exam_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class PlansView(APIView):
    """
    Plans

    METHOD GET - FOR GETTING ALL PLANS
    METHOD POST - FOR ADDING A PLAN
    METHOD PUT - FOR UPDATING A PLAN
    """

    def get(self, request):
        try:
            if request.user.is_superuser:
                plans = Plans.objects.filter(is_deleted=False)
                plans_data = PlanSerializer(plans, many=True)

                return Response(plans_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'You are not authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                plan_name = data['plan_name']
                alternative_name = data['alternative_name']
                price = data['price']
                description = data['description']
                validity = data['validity']

                exam_list = data['exam_list']
                # exams = exam_list.split(",")

                plan = Plans.objects.create(
                    plan_name=plan_name,
                    alternative_name=alternative_name,
                    price=price,
                    description=description,
                    validity=validity,
                    is_deleted=False,
                    is_active=True,
                    created_by=request.user
                )

                if plan:
                    for exam_id in exam_list:
                        plan.exams.add(exam_id)

                    plans = Plans.objects.filter(is_deleted=False)
                    plans_data = PlanSerializer(plans, many=True)

                    return Response(plans_data.data, status=HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                plan_id = data['plan_id']
                plan_name = data['plan_name']
                alternative_name = data['alternative_name']
                price = data['price']
                description = data['description']
                validity = data['validity']
                is_deleted = data['is_deleted']
                is_active = data['is_active']

                if is_deleted == 'true':
                    is_deleted = True
                else:
                    is_deleted = False

                if is_active == 'true':
                    is_active = True
                else:
                    is_active = False

                new_exam_list = data['exams']
                # new_exams = exam_list.split(",")

                plan = Plans.objects.filter(id=plan_id).update(
                    plan_name=plan_name,
                    alternative_name=alternative_name,
                    price=price,
                    description=description,
                    validity = validity,
                    is_active = is_active,
                    is_deleted=is_deleted,
                )

                if plan:
                    plan_update = Plans.objects.get(id=plan_id)
                    all_exams = Exams.objects.all()

                    for exam in all_exams:
                        exam_id = exam.id
                        plan_update.exams.remove(exam_id)

                    for exam_id in new_exam_list:
                        plan_update.exams.add(exam_id)

                    plans = Plans.objects.filter(is_deleted=False)
                    plans_data = PlanSerializer(plans, many=True)

                    return Response(plans_data.data, status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SinglePlanView(APIView):
    """
    This is for getting Single Plan
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            if request.user.is_superuser:
                plan = Plans.objects.get(id=id)
                plan_data = ExamSerializer(plan, many=False)

                return Response(plan_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class PaymentView(APIView):
    """
    Payment View

    METHOD GET - FOR GETTING ALL PAYMENTS
    METHOD POST - FOR ADDING A PAYMENT
    METHOD PUT - FOR UPDATING A PAYMENT
    """

    def get(self, request):
        try:
            if request.user.is_superuser:
                payment = Payment.objects.all()
                payment_data = PaymentSerializer(payment, many=True)

                return Response(payment_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'You are not authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                user_id = data['user_id']
                plan_id = data['plan_id']
                payment_for = data['payment_for']
                payment_amount = data['payment_amount']
                payment_id = data['payment_id']
                payment_gateway = data['payment_gateway']
                payment_status = data['payment_status']
                bank_ref_num = data['bank_ref_num']
                pg_type = data['pg_type']
                pay_mode = data['pay_mode']
                paid_on = data['paid_on']
                expire_on = data['expire_on']

                payment = Payment.objects.create(
                    user_id = user_id,
                    plan_id = plan_id,
                    payment_for = payment_for,
                    payment_amount = payment_amount,
                    payment_id = payment_id,
                    payment_gateway = payment_gateway,
                    payment_status = payment_status,
                    bank_ref_num = bank_ref_num,
                    pg_type = pg_type,
                    pay_mode = pay_mode,
                    paid_on = paid_on,
                    expire_on = expire_on,
                )

                if payment:
                    return JsonResponse({'status': 1, 'message': 'payment done', 'id': payment.id},
                                        status=HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def put(self, request):
        data = json.loads(request.body)
        try:
            if request.user.is_superuser:
                pay_id = data['pay_id']
                user_id = data['user_id']
                plan_id = data['plan_id']
                payment_for = data['payment_for']
                payment_amount = data['payment_amount']
                payment_id = data['payment_id']
                payment_gateway = data['payment_gateway']
                payment_status = data['payment_status']
                bank_ref_num = data['bank_ref_num']
                pg_type = data['pg_type']
                pay_mode = data['pay_mode']
                paid_on = data['paid_on']
                expire_on = data['expire_on']

                payment = Payment.objects.filter(id=pay_id).update(
                    user_id=user_id,
                    plan_id=plan_id,
                    payment_for=payment_for,
                    payment_amount=payment_amount,
                    payment_id=payment_id,
                    payment_gateway=payment_gateway,
                    payment_status=payment_status,
                    bank_ref_num=bank_ref_num,
                    pg_type=pg_type,
                    pay_mode=pay_mode,
                    paid_on=paid_on,
                    expire_on=expire_on,
                )

                if payment:
                    return JsonResponse({'status': 1, 'message': 'updated'},
                                        status=HTTP_200_OK)
                else:
                    return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class SinlePaymentView(APIView):
    """
    This is for getting Single Exam Details
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            if request.user.is_superuser:
                payment = Payment.objects.get(id=id)
                payment_data = ExamSerializer(payment, many=False)

                return Response(payment_data.data, status=HTTP_200_OK)

            else:
                return JsonResponse({'status': 0, 'message': 'Not Authorized'}, status=HTTP_401_UNAUTHORIZED)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


class VideosView(APIView):
    """
    All Vidoes Collections View

    METHOD GET - FOR GETTING ALL VIDEO LECTURES
    METHOD POST - FOR ADDING A VIDEO LECTURE
    METHOD PUT - FOR UPDATING A VIDEO LECTURE
    """

    def get(self, request):
        """
        This Method will gives 100 Entries of Videos
        page will start from 1 here in this method
        :param request: page=1/2/3....
        :return: List of Videos
        """
        page = request.GET.get('page')

        if request.method == 'GET' and 'is_deleted' in request.GET:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                videos = Videos.objects.filter(is_deleted=False).order_by('title')[offset:limit]
                videos_data = VideoSerializer(videos, many=True)

                return Response(videos_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)
        else:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                videos = Videos.objects.all().order_by('title')[offset:limit]
                videos_data = VideoSerializer(videos, many=True)

                return Response(videos_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)

        try:
            title = data['title']
            video_alt_title = data['video_alt_title']
            description = data['description']
            link = data['link']
            subject_id = data['subject_id']

            topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            video = Videos.objects.create(
                title=title,
                video_alt_title=video_alt_title,
                description=description,
                link=link,
                subject=subject,
                created_by=request.user,
                is_deleted=False,
            )

            if video:
                for topic in topics:
                    video.topics.add(topic)

                return JsonResponse({'status': 1, 'message': 'Video added', 'id': video.id},
                                    status=HTTP_201_CREATED)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)



    def put(self, request):
        data = json.loads(request.body)
        try:
            video_id = data['video_id']
            title = data['title']
            video_alt_title = data['video_alt_title']
            description = data['description']
            link = data['link']
            subject_id = data['subject_id']
            is_deleted = data['is_deleted']

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            new_topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            video = Videos.objects.filter(id=video_id).update(
                title=title,
                video_alt_title=video_alt_title,
                description=description,
                link=link,
                subject=subject,
                is_deleted=is_deleted,
            )

            if video:
                video_update = Videos.objects.get(id=video_id)
                all_topics = Topics.objects.all()

                for topic in all_topics:
                    topic_id = topic.id
                    video_update.topics.remove(topic_id)

                for topic in new_topics:
                    video_update.topics.add(topic)

                videos = Videos.objects.all().order_by('title')[0:100]
                videos_data = VideoSerializer(videos, many=True)

                return Response(videos_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleVideoView(APIView):
    """
    This is for getting Single Video Detail
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            video = Videos.objects.get(id=id)
            video_data = VideoSerializer(video, many=False)

            return Response(video_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_400_BAD_REQUEST)

class SearchVideosView(generics.ListAPIView):
    """
    This view for searching Videos in the Database, by by title, alt_title,link,subject_name,topic_name,created_by,created_at
    """
    queryset = Videos.objects.all().order_by('-id')
    serializer_class = VideoSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'id',
        'title',
        'video_alt_title',
        'link',
        'subject__subject_name',
        'topics__topic_title',
        'created_by__name',
        'created_at'
    )

class HandoutsView(APIView):
    """
    Handouts collections View

    METHOD GET - FOR GETTING ALL HANDOUTS
    METHOD POST - FOR ADDING A HANDOUT
    METHOD PUT - FOR UPDATING A HANDOUT
    """

    def get(self, request):
        """
        This Method will gives 100 Entries of handouts
        page will start from 1 here in this method
        :param request: page=1/2/3....
        :return: List of handouts  
        """
        page = request.GET.get('page')
        if request.method == 'GET' and 'is_deleted' in request.GET:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                handout = Handout.objects.filter(is_deleted=False)[offset:limit]
                handout_data = HandoutSerializer(handout, many=True)

                return Response(handout_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)
        else:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                handout = Handout.objects.all()[offset:limit]
                handout_data = HandoutSerializer(handout, many=True)

                return Response(handout_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            title = data['title']
            handout_alt_title = data['handout_alt_title']
            description = data['description']
            link = data['link']
            subject_id = data['subject_id']

            topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            handout = Handout.objects.create(
                title=title,
                handout_alt_title=handout_alt_title,
                description=description,
                link=link,
                subject=subject,
                created_by=request.user,
                is_deleted=False,
            )

            if handout:
                for topic in topics:
                    handout.topics.add(topic)

                return JsonResponse({'status': 1, 'message': 'handout added', 'id': handout.id},
                                    status=HTTP_201_CREATED)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)



    def put(self, request):
        data = json.loads(request.body)
        try:
            handout_id = data['handout_id']
            title = data['title']
            handout_alt_title = data['handout_alt_title']
            description = data['description']
            link = data['link']
            subject_id = data['subject_id']
            is_deleted = data['is_deleted']

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            new_topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            handout = Handout.objects.filter(id=handout_id).update(
                title=title,
                handout_alt_title=handout_alt_title,
                description=description,
                link=link,
                subject=subject,
                is_deleted=is_deleted,
            )

            if handout:
                handout_update = Handout.objects.get(id=handout_id)
                all_topics = Topics.objects.all()

                for topic in all_topics:
                    topic_id = topic.id
                    handout_update.topics.remove(topic_id)

                for topic in new_topics:
                    handout_update.topics.add(topic)

                handout = Handout.objects.all()[0:100]
                handout_data = HandoutSerializer(handout, many=True)

                return Response(handout_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleHandoutView(APIView):
    """
    This is for getting HANDOUT
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            handout = Handout.objects.get(id=id)
            handout_data = HandoutSerializer(handout, many=False)

            return Response(handout_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'No handout find'}, status=HTTP_502_BAD_GATEWAY)

class SearchHandoutView(generics.ListAPIView):
    """
    This view for searching Handout in the Database, by title, alt_title,link,subject_name,topic_name,created_by,created_at
    """
    queryset = Handout.objects.all().order_by('-id')
    serializer_class = HandoutSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'id',
        'title',
        'handout_alt_title',
        'link',
        'subject__subject_name',
        'topics__topic_title',
        'created_by__name',
        'created_at'
    )


class QuestionOptionView(APIView):
    """
    Payment View

    METHOD GET - FOR GETTING ALL OPTIONS
    METHOD POST - FOR ADDING A OPTION
    METHOD PUT - FOR UPDATING A OPTION
    """

    def get(self, request):
        page = request.GET.get('page')

        if request.method == 'GET' and 'is_deleted' in request.GET:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                question_option = QuestionOptions.objects.filter(is_deleted=False)[offset:limit]
                question_option_data = QuestionOptionSerializer(question_option, many=True)

                return Response(question_option_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)
        else:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                question_option = QuestionOptions.objects.all()[offset:limit]
                question_option_data = QuestionOptionSerializer(question_option, many=True)

                return Response(question_option_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)
        try:
            option_title = data['option_title']
            hindi_option_title = data['hindi_option_title']

            question_option = QuestionOptions.objects.create(
                option_title=option_title,
                hindi_option_title=hindi_option_title,
                created_by=request.user,
                is_deleted=False,
            )

            if question_option:
                question_option = QuestionOptions.objects.all()[0:100]
                question_option_data = QuestionOptionSerializer(question_option, many=True)

                return Response(question_option_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


    def put(self, request):
        data = json.loads(request.body)
        try:
            question_option_id = data['option_id']
            option_title = data['option_title']
            hindi_option_title = data['hindi_option_title']
            is_deleted = data['is_deleted']

            if is_deleted == 'true':
                is_deleted = True
            else:
                is_deleted = False

            option = QuestionOptions.objects.filter(id=question_option_id).update(
                option_title=option_title,
                hindi_option_title=hindi_option_title,
                is_deleted=is_deleted,
            )

            if option:
                question_option = QuestionOptions.objects.all()[0:100]
                question_option_data = QuestionOptionSerializer(question_option, many=True)

                return Response(question_option_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleQuestionOptionView(APIView):
    """
    This is for getting OPTION
    """

    def get(self, request):

        id = request.GET.get('id')

        try:
            option = QuestionOptions.objects.get(id=id)
            option_data = QuestionOptionSerializer(option, many=False)

            return Response(option_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'No handout find'}, status=HTTP_502_BAD_GATEWAY)

class SearchQuestionOptionView(generics.ListAPIView):
    """
    This view for searching Options in the Database
    """
    queryset = QuestionOptions.objects.all().order_by('-id')
    serializer_class = QuestionOptionSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'id',
        'option_title',
        'created_by__name',
        'created_at'
    )

class QuestionsView(APIView):
    """
    Payment View

    METHOD GET - FOR GETTING ALL QUESTIONS/ QUESTION BANK
    METHOD POST - FOR ADDING A QUESTION
    METHOD PUT - FOR UPDATING A QUESTION
    """

    def get(self, request):
        page = request.GET.get('page')

        if request.method == 'GET' and 'is_deleted' in request.GET:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                questions = Questions.objects.filter(is_deleted=False)[offset:limit]
                questions_data = QuestionSerializer(questions, many=True)

                return Response(questions_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)
        else:
            try:
                limit = 100 * int(page)
                offset = 100 * int(int(page) - 1)

                questions = Questions.objects.all()[offset:limit]
                questions_data = QuestionSerializer(questions, many=True)

                return Response(questions_data.data, status=HTTP_200_OK)
            except:
                return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

    def post(self, request):
        data = json.loads(request.body)

        try:
            question = data['question']
            hindi_question = data['hindi_question']
            solution = data['solution']
            hindi_solution = data['hindi_solution']
            subject_id = data['subject']
            question_type = data['question_type']
            correct_marks = data['correct_marks']
            negative_marks = data['negative_marks']
            is_negative_marking = data['is_negative_marking']

            if is_negative_marking == 'true':
                is_negative_marking = True
            else:
                is_negative_marking = False

            topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            question = Questions.objects.create(
                question=question,
                hindi_question=hindi_question,
                solution=solution,
                hindi_solution=hindi_solution,
                subject=subject,
                question_type=question_type,
                correct_marks=correct_marks,
                negative_marks=negative_marks,
                is_negative_marking=is_negative_marking,
                created_by=request.user,
                is_deleted=False,
            )

            if question:
                for topic in topics:
                    question.topics.add(topic)

                return JsonResponse({'status': 1, 'message': 'question added', 'id': question.id},
                                    status=HTTP_201_CREATED)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not added'}, status=HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)


    def put(self, request):
        data = json.loads(request.body)
        try:
            question_id = data['question_id']
            question = data['question']
            hindi_question = data['hindi_question']
            solution = data['solution']
            hindi_solution = data['hindi_solution']
            subject_id = data['subject']
            question_type = data['question_type']
            correct_marks = data['correct_marks']
            negative_marks = data['negative_marks']
            is_negative_marking = data['is_negative_marking']

            if is_negative_marking == 'true':
                is_negative_marking = True
            else:
                is_negative_marking = False

            topics = data['topics']
            # topics_list = topics.split(",")

            subject = Subjects.objects.get(id=subject_id)

            question = Questions.objects.filter(id=question_id).update(
                question=question,
                hindi_question=hindi_question,
                solution=solution,
                hindi_solution=hindi_solution,
                subject=subject,
                question_type=question_type,
                correct_marks=correct_marks,
                negative_marks=negative_marks,
                is_negative_marking=is_negative_marking,
                is_deleted=False,
            )

            if question:
                question_updated = Questions.objects.get(id=question_id)
                all_topics = Topics.objects.all()

                for topic in all_topics:
                    topic_id = topic.id
                    question_updated.topics.remove(topic_id)

                for topic in topics:
                    question_updated.topics.add(topic)

                updated_question = Questions.objects.get(id=question_id)
                updated_question_data = QuestionSerializer(updated_question, many=False)

                return Response(updated_question_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'Some Error Occurred'}, status=HTTP_502_BAD_GATEWAY)

class SingleQuestionView(APIView):
    """
    This is for getting a QUESTION
    """

    def get(self, request):
        id = request.GET.get('id')
        try:
            question = Questions.objects.get(id=id)
            question_data = QuestionSerializer(question, many=False)

            return Response(question_data.data, status=HTTP_200_OK)

        except:
            return JsonResponse({'status': 0, 'message': 'No Question find'}, status=HTTP_502_BAD_GATEWAY)

class SearchQuestionView(generics.ListAPIView):
    """
    This view for searching Videos in the Database
    """
    queryset = Questions.objects.all().order_by('-id')
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        'id',
        'question',
        'subject__subject_name',
        'topics__topic_title',
        'question_type',
        'correct_marks',
        'created_by__name',
        'created_at'
    )

class QuestionOptionUpdate(APIView):
    """
    This for adding and removing any option
    """
    def post(self, request):
        data = json.loads(request.body)

        try:
            question_id = data['question_id']
            option_id = data['option_id']

            question = Questions.objects.get(id=question_id)
            question_data = QuestionSerializer(question, many=False)

            if question:
                question.options.add(option_id)

                return Response(question_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'No Option find'}, status=HTTP_502_BAD_GATEWAY)

    # This for removing option
    def put(self, request):
        data = json.loads(request.body)

        try:
            question_id = data['question_id']
            option_id = data['option_id']

            question = Questions.objects.get(id=question_id)
            question_data = QuestionSerializer(question, many=False)

            if question:
                question.options.remove(option_id)

                return Response(question_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'No Option find'}, status=HTTP_502_BAD_GATEWAY)

class QuestionCorrectOptionUpdate(APIView):
    """
    This for adding and removing any option
    """
    def post(self, request):
        data = json.loads(request.body)

        try:
            question_id = data['question_id']
            option_id = data['option_id']

            question = Questions.objects.get(id=question_id)
            question_data = QuestionSerializer(question, many=False)

            if question:
                question.correct_options.add(option_id)

                return Response(question_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'No Correct Option find'}, status=HTTP_502_BAD_GATEWAY)

    # This for removing option
    def put(self, request):
        data = json.loads(request.body)

        try:
            question_id = data['question_id']
            option_id = data['option_id']

            question = Questions.objects.get(id=question_id)
            question_data = QuestionSerializer(question, many=False)

            if question:
                question.correct_options.remove(option_id)

                return Response(question_data.data, status=HTTP_200_OK)
            else:
                return JsonResponse({'status': 0, 'message': 'Could not updated'}, status=HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({'status': 0, 'message': 'No Correct Option find'}, status=HTTP_502_BAD_GATEWAY)
