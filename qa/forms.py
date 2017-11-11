from django import forms
from django.conf import settings
from qa.models import Question, UserQAProfile
from django.contrib.auth.models import User


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        try:
            settings.QA_SETTINGS['qa_description_optional']
            self.fields['description'].required = not settings.QA_SETTINGS[
                'qa_description_optional']

        except KeyError:
            pass

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserQAProfile
        fields = ('website', 'points')