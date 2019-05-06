from django.conf.urls import url, include
from .views import *
from .views_2 import *

urlpatterns = [
    url(r'^login', login),
    url(r'^profile', Profile.as_view()),
    url(r'^logout', Logout.as_view()),

    url(r'^exams-category', ExamCategoryView.as_view()),
    url(r'^examCategory', SingleExamCategoryView.as_view()),

    url(r'^subjects', SubjectsView.as_view()),
    url(r'^subject', SingleSubjectView.as_view()),

    url(r'^topics/$', TopicsView.as_view()),
    url(r'^topic', SingleTopicView.as_view()),

    url(r'^exams/$', ExamsView.as_view()),
    url(r'^exam/$', SingleExamView.as_view()),

    url(r'^plans', PlansView.as_view()),
    url(r'^plan', SinglePlanView.as_view()),

    url(r'^payments', PaymentView.as_view()),
    url(r'^payment', SinlePaymentView.as_view()),

    url(r'^videos/$', VideosView.as_view()),
    url(r'^video/$', SingleVideoView.as_view()),
    url(r'^searchVideo/$', SearchVideosView.as_view()),

    url(r'^handouts/$', HandoutsView.as_view()),
    url(r'^handout/$', SingleHandoutView.as_view()),
    url(r'^searchHandout/$', SearchHandoutView.as_view()),

    url(r'^question-options/$', QuestionOptionView.as_view()),
    url(r'^question-option/$', SingleQuestionOptionView.as_view()),
    url(r'^search-question-option/$', SearchQuestionOptionView.as_view()),

    url(r'^questions/$', QuestionsView.as_view()),
    url(r'^question/$', SingleQuestionView.as_view()),
    url(r'^searchQuestion/$', SearchQuestionView.as_view()),
    url(r'^question-option-update/$', QuestionOptionUpdate.as_view()),
    url(r'^question-correct-option-update/$', QuestionCorrectOptionUpdate.as_view()),

    url(r'^lectures-video/$', VideoLectureView.as_view()),
    url(r'^lecture-video/$', SingleVideoLecView.as_view()),
    url(r'^search-video-lecture/$', SearchVideoLecView.as_view()),

    url(r'^notes/$', NotesView.as_view()),
    url(r'^note/$', SingleNotesView.as_view()),
    url(r'^search-notes/$', SearchNotesView.as_view()),

    url(r'^quizzes/$', QuizzesView.as_view()),
    url(r'^quiz/$', SingleQuizView.as_view()),
    url(r'^search-quiz/$', SearchQuizView.as_view()),
]
