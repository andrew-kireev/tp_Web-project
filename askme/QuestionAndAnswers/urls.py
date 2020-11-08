"""QuestionAndAnswers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path
from django.urls import path

from app import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', views.login, name='login'),
    path('new_qustion', views.new_question, name='new-question'),
    path('registration', views.registration, name='registration'),
    path('questions_by_teg/<slug:tag_name>', views.questions_by_teg, name='question-by-teg'),
    path('', views.questions_and_answers, name='main-page'),
    path('hot_questions', views.hot_questions, name='hot-questions'),
    path('one_question_page/<int:page_number>/', views.one_question, name='one-question-page'),
    re_path(r'^one_question_page/(\d+)/$', views.one_question, name='one-question-page'),
    path('settings', views.settings, name='settings'),
    path('test', views.test)
]
