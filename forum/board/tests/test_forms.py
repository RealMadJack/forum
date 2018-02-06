from django.core.exceptions import ValidationError
from test_plus.test import TestCase

from ..forms import TopicForm


class TestTopicForm(TestCase):
    def setUp(self):
        self.clean_message = TopicForm.clean_message
        self.cleaned_data = {'message': ''}

    def test_message_validator(self):
        self.assertRaises(ValidationError, self.clean_message, self)
