from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    """docstring for Topic"""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

