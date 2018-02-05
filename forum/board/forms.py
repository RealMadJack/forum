from django import forms


class TopicForm(forms.Form):
    message = forms.CharField(
        label='Message:',
        max_length=500,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
