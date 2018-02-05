from django import forms


class TopicForm(forms.Form):
    message = forms.CharField(max_length=300)
