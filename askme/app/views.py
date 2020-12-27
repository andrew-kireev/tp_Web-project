from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
# from djangoProject.settings import PER_PAGE
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import *
from .forms import LoginForm, RegistrationForm, SettingsForm, QuestionForm, AnswerForm, AvatarForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout

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
    try:
        que = QuestionManager().get_quest_by_teg(tag_name)
        page_obj, page = paginate(que, request)
        popular_tags = TagManager().get_top_five()
        best_members_ = ProfileManager().get_top_five()
    except:
        raise Http404("")

    return render(request, 'questions_by_teg.html', {
        'questions': page_obj,
        'tag': tag_name,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def questions_and_answers(request):
    try:
        que = QuestionManager().get_newest()
        page_obj, page = paginate(que, request)
        popular_tags = TagManager().get_top_five()
        best_members_ = ProfileManager().get_top_five()
    except:
        raise Http404("")

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

    return render(request, 'hot_questions.html', {
        'questions': page_obj,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def one_question(request, page_number):

    question = QuestionManager().get_que_by_id(int(page_number))
    ans = AnswerManager().get_answers(int(page_number))

    page_obj, page = paginate(ans, request)
    popular_tags = TagManager().get_top_five()
    best_members_ = ProfileManager().get_top_five()

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid() and request.user.is_authenticated:
            que = Question.objects.get(id=page_number)
            answer = Answer.objects.create(Author=request.user.profile,
                                           question=que,
                                           text=form.cleaned_data['text'])
            que.answers_count += 1
            que.save()
            answer.save()
            print(page)
            return redirect(reverse('one-question-page', kwargs={'page_number': que.pk})
            + f"?page={len(page_obj)}")

    return render(request, 'one_question_page.html', {
        'form': form,
        'question': question[0],
        'answers': page_obj,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            print("логинемся")
            print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('main-page')

    popular_tags = TagManager().get_top_five()
    best_members_ = ProfileManager().get_top_five()

    return render(request, 'login.html', {
        'user': request.user,
        'form': form,
        'tags': popular_tags,
        'best_members': best_members_,
    })


@login_required
def new_question(request):
    popular_tags = TagManager().get_top_five()
    best_members_ = ProfileManager().get_top_five()

    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = Question.objects.create(Author=request.user.profile,
                                               title=form.cleaned_data['title'],
                                               text=form.cleaned_data['text'])
            tags = form.cleaned_data['tags']
            question.tags.set(tags)
            question.save()
            print(question.tags)
            return redirect(reverse('one-question-page', kwargs={'page_number': question.pk}))

    return render(request, 'new_question.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


def registration(request):
    popular_tags = TagManager().get_top_five()
    best_members_ = ProfileManager().get_top_five()

    if request.method == 'GET':
        form = RegistrationForm()
        avatar_form = AvatarForm()
        print('tut')
    else:
        print("регистрируемся")
        form = RegistrationForm(data=request.POST, files=request.FILES)
        # avatar_form = AvatarForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user, profile = form.save()
            auth.login(request, user)
            # avatar_form.save()
            return redirect("main-page")

    return render(request, 'registration.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members_
    })


@login_required
def settings(request):
    popular_tags = TagManager().get_top_five()
    best_members_ = ProfileManager().get_top_five()

    if request.method == 'GET':
        form = SettingsForm()
        avatar_form = AvatarForm()
        print('tut')
    else:
        print("регистрируемся")
        form = SettingsForm(data=request.POST)
        avatar_form = AvatarForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        print(request.FILES)
        if form.is_valid():
            user = request.user
            print('валидный')
            if form.cleaned_data["login"] != user.username and form.cleaned_data["login"] != '':
                user.name = form.cleaned_data["login"]
            if form.cleaned_data["username"] != user.username and form.cleaned_data["username"] != '':
                user.username = form.cleaned_data["username"]
            if form.cleaned_data["email"] != user.email and form.cleaned_data["email"] != '':
                user.email = form.cleaned_data["email"]
            if form.cleaned_data["password"] != '':
                user.set_password(form.cleaned_data["password"])
            user.save()
            auth.login(request, user)
            # if avatar_form.get('avatar', None) is not None:
            avatar_form.save()

    return render(request, 'settings.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members_,
        'avatar_form': avatar_form
    })


@login_required
def logout(request):
    django_logout(request)
    return redirect("main-page")


@require_POST
@login_required
def like_question(request):
    data = request.POST
    if Like.objects.filter(user=request.user.profile, question_id=data['qid']).exists():
        print('Уже существует')
        question = Question.objects.get(pk=data['qid'])
        return JsonResponse({'questions_likes': question.likes})
    print('\n\n', '=' * 100)
    print(data)
    print('=' * 100, '\n\n')
    like = Like.objects.create(user=request.user.profile, question_id=data['qid'])
    print(like)
    like.save()
    question = Question.objects.get(pk=data['qid'])
    question.likes += 1
    question.save()
    print(question)

    return JsonResponse({'questions_likes': question.likes})


@require_POST
@login_required
def like_one_question(request, page_number):
    data = request.POST
    if Like.objects.filter(user=request.user.profile, question_id=data['qid']).exists():
        print('Уже существует')
        question = Question.objects.get(pk=data['qid'])
        return JsonResponse({'questions_likes': question.likes})
    print('\n\n', '=' * 100)
    print(data)
    print('=' * 100, '\n\n')
    like = Like.objects.create(user=request.user.profile, question_id=data['qid'])
    print(like)
    like.save()
    question = Question.objects.get(pk=data['qid'])
    question.likes += 1
    question.save()
    print(question)

    return JsonResponse({'questions_likes': question.likes})


@require_POST
@login_required
def like_answer(request, page_number):
    data = request.POST
    if AnswersLikes.objects.filter(user=request.user.profile, answer_id=data['qid']).exists():
        print('Уже существует')
        answer = Answer.objects.get(pk=data['qid'])
        return JsonResponse({'questions_likes': answer.likes})
    print('\n\n', '=' * 100)
    print(data)
    print('=' * 100, '\n\n')
    like = AnswersLikes.objects.create(user=request.user.profile, answer_id=data['qid'])
    print(like)
    like.save()
    answer = Answer.objects.get(pk=data['qid'])
    answer.likes += 1
    answer.save()
    print(answer)

    return JsonResponse({'answers_likes': answer.likes})


@require_POST
@login_required
def is_correct_answer(request, page_number):
    data = request.POST
    print(data)
    current_answer = Answer.objects.get(pk=data['id'])
    if current_answer.is_correct:
        current_answer.is_correct = False
    else:
        current_answer.is_correct = True
    current_answer.save()
    print(current_answer.is_correct)
    return JsonResponse({'is_correct': current_answer.is_correct})


def test(request):
    return render(request, 'inc/base.html', {})
