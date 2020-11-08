from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
# from djangoProject.settings import PER_PAGE
from django.http import HttpResponse
from .models import *

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
        'text': text,
        'tags': ['tag' + str(i), 'tag'],
        'id': int(i)
    })

    answers = []
    for i in range(0, 30):
        answers.append({
            'text': text
        })

one_page_question = [{'title': 'title1',
                      'id': 423,
                      'text': 'What type of music are you into?',
                      'tag': 'tag1',
                      'tags': ['tag1', 'tag5']},
                     {'title': 'title2',
                      'id': 424,
                      'text': 'What was the best vacation you ever took and why?',
                      'tag': 'tag1',
                      'tags': ['tag1', 'tag8']},
                     {'title': 'title3',
                      'id': 43,
                      'text': 'Do you like going to the movies or prefer watching at home?',
                      'tag': 'tag2',
                      'tags': ['tag2', 'tag20']},
                     {'title': 'title4',
                      'id': 433,
                      'text': 'What’s your favorite thing about your current job?',
                      'tag': 'tag2',
                      'tags': ['tag2', 'tag99']},
                     {'title': 'title5',
                      'id': 323,
                      'text': 'What do you remember most about your first job?',
                      'tag': 'tag2',
                      'tags': ['tag2', 'tag17']}]

popular_tags_ = ['python',
                'C++',
                'Linux',
                'TechnoPark',
                'MailRu',
                'Golang',
                'Ngnix',
                'Docker']

best_members = ['Pavel Durov',
                'Elon Mask',
                'Linus Torvalds',
                'Anton']



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


def questions_by_teg(request, tag_name):
    que = QuestionManager().get_quest_by_teg(tag_name)
    questions_ = []
    # for item in one_page_question:
    #     if item['tag'] == tag_name:
    #         questions_.append(item)

    page_obj, page = paginate(que, request)
    popular_tags = TagManager().get_top_five()

    # print(page_obj)
    # print(tag_name)

    return render(request, 'questions_by_teg.html', {
        'questions': page_obj,
        'tag': tag_name,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def questions_and_answers(request):
    que = QuestionManager().get_most_popular()
    page_obj, page = paginate(que, request)

    popular_tags = TagManager().get_top_five()

    best_members_ = ProfileManager().get_top_five()

    # print(que[0].creation_date)
    # print(que[1].creation_date)

    return render(request, 'questions_and_answers.html', {
        'questions': page_obj,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def hot_questions(request):
    que = QuestionManager().get_most_popular()
    page_obj, page = paginate(que, request)

    popular_tags = TagManager().get_top_five()

    best_members_ = ProfileManager().get_top_five()

    # print(que[0].creation_date)
    # print(que[1].creation_date)

    return render(request, 'hot_questions.html', {
        'questions': page_obj,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def one_question(request, page_number):
    question = QuestionManager().get_que_by_id(int(page_number))
    # print(question)
    ans = AnswerManager().get_answers(int(page_number))
    print(ans)

    page_obj, page = paginate(ans, request)
    popular_tags = TagManager().get_top_five()

    # print(question[0].title)
    # print(page)

    return render(request, 'one_question_page.html', {
        'question': question[0],
        'answers': page_obj,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def login(request):
    popular_tags = TagManager().get_top_five()

    return render(request, 'login.html', {
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def new_question(request):
    popular_tags = TagManager().get_top_five()

    return render(request, 'new_question.html', {
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def registration(request):
    popular_tags = TagManager().get_top_five()

    return render(request, 'registration.html', {
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def settings(request):
    popular_tags = TagManager().get_top_five()

    return render(request, 'settings.html', {
        'popular_tags': popular_tags,
        'best_members': best_members
    })


def test(request):
    return render(request, 'inc/base.html', {})
