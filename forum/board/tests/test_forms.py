from django.core.exceptions import ValidationError
from test_plus.test import TestCase

from ..forms import TopicForm


class TestTopicForm(TestCase):

    def setUp(self):
        self.clean_message = TopicForm.clean_message

    def test_message_validator_empty(self):
        self.cleaned_data = {'message': ''}

        self.assertRaises(ValidationError, self.clean_message, self)

    def test_message_validator_normal(self):
        self.cleaned_data = {'message': 'test string'}
        clean_data = self.clean_message(self)
        # Func should return legit string
        self.assertEqual(clean_data, self.cleaned_data['message'])
