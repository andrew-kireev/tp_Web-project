from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)
admin.site.register(AnswersLikes)


# Register your models here.
