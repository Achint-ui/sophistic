from django.forms import ModelForm
from django import forms
from .models import Topic, Comment
class TopicForm(ModelForm):
    topic = forms.CharField(widget=forms.TextInput, label='')

    class  Meta:
        model = Topic
        fields = ['topic']

class CommentForm(ModelForm):
    body = forms.CharField(widget=forms.TextInput, label='')
    class Meta:
        model = Comment
        fields = ['body']