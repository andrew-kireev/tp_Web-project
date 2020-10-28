from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login(request):
    return render(request, 'login.html', {})

def new_question(request):
    return render(request, 'new_question.html', {})

def test(request):
    return render(request, 'inc/base.html', {})