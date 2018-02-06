from django import forms


class TopicForm(forms.Form):
    message = forms.CharField(
        label='Message:',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': '4'}),
    )

    def clean_message(self):
        data = self.cleaned_data['message']
        if data <= 0:
            print('Message must contain at least 1 symbol.')
            raise forms.ValidationError('Message must contain at least 1 symbol.')
        return data
