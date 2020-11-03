from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
# from djangoProject.settings import PER_PAGE
from django.http import HttpResponse
# Create your views here.


text = 'Lorem ipsum dolor sit, amet consectetur adipisicing elit.' \
       'Officiis, modi maiores dolores blanditiis voluptatum rerum, \
                assumenda tempore laborum odio quia dolorum \
                soluta illo quae reiciendis eligendi ratione ab recusandae debitis!'

questions = []
for i in range(0, 30):
  questions.append({
    'title': 'title' + str(i),
    'id': i,
    'text': text
  })

  answers = []
  for i in range(0, 30):
      answers.append({
          'text': text
      })

one_page_question = [{'title': 'title1',
                      'text': 'What type of music are you into?'},
                     {'title': 'title2',
                      'text': 'What was the best vacation you ever took and why?'},
                     {'title': 'title3',
                      'text': 'Do you like going to the movies or prefer watching at home?'},
                     {'title': 'title4',
                      'text': 'What’s your favorite thing about your current job?'},
                     {'title': 'title5',
                      'text': 'What do you remember most about your first job?'}]






def paginate(objects_list, request):
    page_number = request.GET.get('page')
    if (page_number == None):
        page_number = 1

    paginator = Paginator(objects_list, 4)
    if (paginator.num_pages == 0):
        return None, None
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except InvalidPage:
        page = paginator.page(1)

    return page.object_list, page

def questions_by_teg(request):
    page_obj, page = paginate(questions, request)

    return render(request, 'questions_by_teg.html', {
        'questions' : page_obj,
        'page' : page
    })



def questions_and_answers(request):
    page_obj, page = paginate(questions, request)

    return render(request, 'questions_and_answers.html', {
        'questions' : page_obj,
        'page' : page
    })

def one_question(request, page_number):
    page_obj, page = paginate(answers, request)
    question = one_page_question[int(page_number)]

    print(question)

    return render(request, 'one_question_page.html',  {
        'question' : question,
        'answers' : page_obj,
        'page' : page
    })

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