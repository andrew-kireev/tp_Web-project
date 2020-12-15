from django import forms
import re
from .models import *
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if ' ' in username:
            raise forms.ValidationError("Whitespaces")
        try:
            user = User.objects.filter(username=username).get()
        except User.DoesNotExist:
            raise forms.ValidationError("User doesn't exist")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("User doesn't exist")
        password = self.cleaned_data["password"]
        user = User.objects.filter(username=username).get()
        if not user.check_password(password):
            raise forms.ValidationError("Wrong password")
        return password


class SettingsForm(forms.Form):
    login = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = ""

    def clean_login(self):
        login = self.cleaned_data['login']
        if login.strip() == '':
            raise forms.ValidationError('Login is empty', code='validation_error')

        return login

    def clean_username(self):
        username = self.cleaned_data['username']

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        return password

    def clean_email(self):
        email = self.cleaned_data['email']

        return email


class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text']


    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['text'].label = ""
        self.fields['tags'].label = ""


    def clean_tags(self):
        tags = self.cleaned_data['tags']
        # tags_ = tags.split(' ')
        pattern = re.compile(r" |,")
        # tags_ = re.split(' |\\,', tags)
        tags_ = pattern.split(tags)
        tags_set = list()
        for tag_name in tags_:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag is not None:
                tags_set.append(tag)
            else:
                tag = Tag.objects.create(name=tag_name)
                tags_set.append(tag)
        print(len(tags_set))
        return tags_set


class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""

    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg'
                    # 'style': 'height: 400px'
                }
            ),
        }



class RegistrationForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        if ' ' in password:
            raise forms.ValidationError('Password contains space.', code='space in password')

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')
        if ' ' in email:
            raise forms.ValidationError('Email contains space.', code='space in email')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        r_password = cleaned_data.get('repeatPassword')

        if password != r_password:
            raise forms.ValidationError('These passwords do not match.')

    def save(self):
        new_user = User(username=self.cleaned_data.get('username'),
                        email=self.cleaned_data.get('email'),
                        password=self.cleaned_data.get('password'))

        username = self.clean_username()
        profile = Profile(user=new_user, name=username)
        new_user.save()
        profile.save()
        return new_user, profile
