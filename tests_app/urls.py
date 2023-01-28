from django.urls import path

from .views import (
    ThemeListView,
    ThemeDetailView,
    QuestionListView,
    QuestionCreateView,
    QuestionRandomListView,
    TestListView,
    TestCreateView,
    TestCreateRandomView,
    TestDetailView,
)


urlpatterns = [
    path('', QuestionListView.as_view(), name='home'),
    path('theme/', ThemeListView.as_view(), name='themes'),
    path('theme/<str:theme>/', ThemeDetailView.as_view(), name='theme_detail'),
    path('question/add/', QuestionCreateView.as_view(), name='question_add'),
    path('question/random/', QuestionRandomListView.as_view(), name='question_random'),
    path('test/', TestListView.as_view(), name='test_list'),
    path('test/create/', TestCreateView.as_view(), name='test_create'),
    path('test/create-random/', TestCreateRandomView.as_view(), name='test_create_random'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
]
