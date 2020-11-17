from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *
from random import choice
from django.utils import timezone
from faker import Faker
from random import randint

f = Faker()


class Command(BaseCommand):
    help = 'Fill database'

    def add_arguments(self, parser):
        parser.add_argument('--tags', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--likes', type=int)
        parser.add_argument('--amount', type=int)
        parser.add_argument('--answers_likes', type=int)

    def create_tags(self, tags_amount):
        for _ in range(tags_amount):
            tag = Tag(name=f.word())
            tag.save()

    def create_users(self, users_amount):
        for i in range(users_amount):
            user = User(username=(f.name() + str(i)), password=f.password(), email=f.email())
            user.save()

            profile = Profile(user=user, name=f.name(),
                              img='https://picsum.photos/640/360')
            profile.save()

    def create_questions(self, questions_amount):
        users = list(Profile.objects.values_list(
                'id', flat=True
        ))
        tags = list(Tag.objects.values_list(
            'id', flat=True
        ))
        for _ in range(questions_amount):
            question = Question.objects.create(
                Author_id=choice(users), title=f.sentence(), text=f.text())
            tags_number = randint(1, 6)
            for _ in range(tags_number):
                tag = Tag.objects.get(pk=choice(tags))
                question.tags.add(tag)
                tag.rating += 1
                tag.save()
            question.save()

    def create_answers(self, answers_amount):
        users = list(Profile.objects.values_list(
            'id', flat=True
        ))
        questions = list(Question.objects.values_list(
            'id', flat=True
        ))
        for _ in range(answers_amount):
            question_id = choice(questions)
            answer = Answer.objects.create(
                Author_id=choice(users), text=f.text(),
                question_id=question_id
            )
            answer.save()
            question = Question.objects.get(pk=question_id)
            question.answers_count += 1
            question.save()

    def create_likes(self):
        users = list(Profile.objects.values_list(
            'id', flat=True
        ))

        questions = list(Question.objects.values_list(
            'id', flat=True
        ))
        for i in questions:
            likes_amount = randint(5, len(users))
            if likes_amount > 5:
                likes_amount = 5
            likes_for_question = list()
            for j in range(likes_amount):
                id_user = choice(users)
                if (id_user) not in likes_for_question:
                    likes_for_question.append(id_user)
                like = Like.objects.create(user_id=id_user, question_id=i)
                like.save()
                question = Question.objects.get(pk=i)
                question.likes += 1
                question.save()

    def create_answers_likes(self):
        users = list(Profile.objects.values_list(
            'id', flat=True
        ))

        answers = list(Answer.objects.values_list(
            'id', flat=True
        ))
        for i in answers:
            likes_amount = randint(1, 5)
            # if likes_amount > 5:
            #     likes_amount = 5
            likes_for_answer = list()
            for j in range(likes_amount):
                id_user = choice(users)
                if (id_user) not in likes_for_answer:
                    likes_for_answer.append(id_user)
                else:
                    continue
                like = AnswersLikes.objects.create(user_id=id_user, answer_id=i)
                like.save()
                answer = Answer.objects.get(pk=i)
                answer.likes += 1
                answer.save()



    def handle(self, *args, **options):
        number_of_tags = options['tags']
        users_amount = options['users']
        questions_amount = options['questions']
        answers_amount = options['answers']
        likes = options['likes']
        answers_likes = options['answers_likes']
        amount = options['amount']

        if amount != None:
            self.create_tags(amount)
            self.create_users(amount)
            self.create_questions(amount)
            self.create_answers(amount)
            self.create_likes()

        if number_of_tags != None:
            self.create_tags(number_of_tags)
        if users_amount != None:
            self.create_users(users_amount)
        if questions_amount != None:
            self.create_questions(questions_amount)
        if answers_amount != None:
            self.create_answers(answers_amount)
        if likes != None:
            self.create_likes()
        if answers_likes != None:
            self.create_answers_likes()