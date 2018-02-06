from django import forms


class TopicForm(forms.Form):
    message = forms.CharField(
        label='Message:',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'rows': '4'}),
    )

    def clean_message(self):
        data = self.cleaned_data['message']
        if len(data) <= 0:
            raise forms.ValidationError('Message must contain at least 1 symbol.')
        return data
