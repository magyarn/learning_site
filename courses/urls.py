from django.contrib import admin
from django.conf.urls import url

from . import views

app_name='courses'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^courses/$', views.CourseListView.as_view(), name="list"),
    url(r'^subject/(?P<subject_slug>\w+)/$', views.SubjectDetailView.as_view(), name="subject_detail"),
    url(r'^suggest/$', views.suggestion_view, name="suggestion_form"),
    url(r'(?P<course_pk>\d+)/text-step/(?P<pk>\d+)/delete/$', views.TextDeleteView.as_view(), name="delete_text"),
    url(r'(?P<course_pk>\d+)/text-step/(?P<pk>\d+)/$', views.TextDetailView.as_view(), name="text_detail"),
    url(r'(?P<course_pk>\d+)/text-create/$', views.TextCreateView.as_view(), name="create_text"),
    url(r'(?P<course_pk>\d+)/text-edit/(?P<pk>\d+)/$', views.TextEditView.as_view(), name="edit_text"),
    url(r'(?P<course_pk>\d+)/quiz-step/(?P<step_pk>\d+)/$', views.quiz_detail, name="quiz_detail"),
    url(r'(?P<course_pk>\d+)/quiz-create/$', views.quiz_create, name="create_quiz"),
    url(r'(?P<course_pk>\d+)/quiz-edit/(?P<quiz_pk>\d+)/$', views.quiz_edit, name="quiz_edit"),
    url(r'(?P<quiz_pk>\d+)/create-question/(?P<question_type>mc|tf)/$',
        views.question_create, name="create_question"),
    url(r'(?P<quiz_pk>\d+)/question-edit/(?P<question_pk>\d+)/$', views.question_edit, name="edit_question"),
    url(r'(?P<question_pk>\d+)/create-answer/', views.answer_create, name="create_answer"),
    url(r'course-create/$', views.CourseCreateView.as_view(), name="create_course"),
    url(r'(?P<pk>\d+)/course-edit/$', views.CourseEditView.as_view(), name="edit_course"),
    url(r'(?P<pk>\d+)/course-delete/$', views.CourseDeleteView.as_view(), name="delete_course"),
    url(r'(?P<userId>\d+)/my-courses/$', views.MyCoursesListView.as_view(), name="my_courses"),
    url(r'by/(?P<teacher>[-\w]+)/$', views.courses_by_teacher, name="courses_by_teacher"),
    url(r'search/$', views.search_results, name="search_results"),
    url(r'^api/v1/course-list/$', views.ListCreateCourse.as_view(), name="course_list_api"),
    url(r'^api/v1/course-list/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyCourse.as_view(), name="course_detail_api"),
    url(r'^api/v1/course-list/(?P<course_pk>\d+)/review-list/$',
        views.ListCreateReview.as_view(), name="review_list_api"),
    url(r'^api/v1/course-list/(?P<course_pk>\d+)/review-list/(?P<pk>\d+)$',
        views.RetrieveUpdateDestroyReview.as_view(), name="review_detail_api"),
    url(r'(?P<pk>\d+)/$', views.CourseDetailView.as_view(), name="detail"),
]
