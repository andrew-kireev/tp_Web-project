from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def questions_by_teg(request):
    return render(request, 'questions_by_teg.html', {})

def questions_and_answers(request):
    return render(request, 'questions_and_answers.html', {})

def one_question(request):
    return render(request, 'one_question_page.html', {})

def login(request):
    return render(request, 'login.html', {})

def new_question(request):
    return render(request, 'new_question.html', {})

def registration(request):
    return render(request, 'registration.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def test(request):
    return render(request, 'inc/base.html', {})