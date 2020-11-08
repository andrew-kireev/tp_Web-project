from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class QuestionManager(models.Manager):
    def get_most_popular(self):
        return Question.objects.all().order_by('-creation_date').reverse()

    def get_quest_by_teg(self, tag):
        questions = Question.objects.filter(tags__name=tag)
        return questions

    def get_que_by_id(self, index):
        return Question.objects.filter(pk=index)


class AnswerManager(models.Manager):
    def get_answers(self, index):
        return Answer.objects.all().filter(question__pk=index).all()


class TagManager(models.Manager):
    def get_top_five(self):
        return Tag.objects.all()[:10]


class ProfileManager(models.Manager):
    def get_top_five(self):
        return Profile.objects.all()[:10]



class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='Tag name')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=256)
    img = models.ImageField(default='askme/static/img/profile.jpeg', blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name='Title')
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='Date of creation')
    text = models.TextField(verbose_name='Text')
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title


class Answer(models.Model):
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='Date of creation')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)



