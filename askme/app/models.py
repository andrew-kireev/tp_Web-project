from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime


class QuestionManager(models.Manager):
    def get_most_popular(self):
        return Question.objects.all().order_by('-likes')

    def get_newest(self):
        return Question.objects.all().order_by('-creation_date')

    def get_quest_by_teg(self, tag):
        questions = Question.objects.filter(tags__name=tag)
        return questions

    def get_que_by_id(self, index):
        return Question.objects.filter(pk=index)


class LikeManager(models.Manager):
    pass


class LikeAnswerManager(models.Manager):
    pass


class AnswerManager(models.Manager):
    def get_answers(self, index):
        return Answer.objects.all().filter(question__pk=index).all().order_by('-likes')


class TagManager(models.Manager):
    def get_top_five(self):
        return Tag.objects.all().order_by('-rating')[:10]


class ProfileManager(models.Manager):
    def get_top_five(self):
        return Profile.objects.all()[:5]


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='Tag name')
    rating = models.IntegerField(default=0)
    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=256)
    avatar = models.ImageField(default='img/default_avatar.jpg', upload_to='avatar/%y/%m/%d')
    objects = ProfileManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name='Title')
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='Date of creation')
    text = models.TextField(verbose_name='Text')
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title


class Answer(models.Model):
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Text')
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='Date of creation')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    objects = AnswerManager()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    objects = LikeManager()


class AnswersLikes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    objects = LikeAnswerManager()
