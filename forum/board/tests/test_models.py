from django.urls import reverse
from test_plus.test import TestCase

from ..models import Board, Category, Topic, Post


class TestBoard(TestCase):

    def setUp(self):
        self.board = Board(name='test board')
        self.board.save()
        self.board1 = Board(name='test board')
        self.board1.save()

    def test_board_unique_slugify(self):
        self.assertEqual(self.board.slug, 'test-board')
        self.assertEqual(self.board1.slug, 'test-board-1')

    def test_absolute_url(self):
        absolute_url = self.board.get_absolute_url()
        reverse_url = reverse('board:board', kwargs={
            'board_slug': self.board.slug
        })
        self.assertEqual(absolute_url, reverse_url)


class TestCategory(TestCase):

    def setUp(self):
        self.board = Board(name='test board')
        self.board.save()
        self.category = Category(board=self.board, name='test category')
        self.category.save()
        self.category1 = Category(board=self.board, name='test category')
        self.category1.save()

    def test_category_unique_slugify(self):
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(self.category1.slug, 'test-category-1')

    def test_absolute_url(self):
        absolute_url = self.category.get_absolute_url()
        reverse_url = reverse('board:category', kwargs={
            'board_slug': self.board.slug,
            'category_slug': self.category.slug
        })
        self.assertEqual(absolute_url, reverse_url)


class TestTopic(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.board = Board(name='test board')
        self.board.save()
        self.category = Category(board=self.board, name='test category')
        self.category.save()
        self.topic = Topic(user=self.user, category=self.category, name='test topic', message='test topic message')
        self.topic.save()
        self.topic1 = Topic(user=self.user, category=self.category, name='test topic', message='test topic message')
        self.topic1.save()

    def test_topic_unique_slugify(self):
        self.assertEqual(self.topic.slug, 'test-topic')
        self.assertEqual(self.topic1.slug, 'test-topic-1')

    def test_absolute_url(self):
        absolute_url = self.topic.get_absolute_url()
        reverse_url = reverse('board:topic', kwargs={
            'board_slug': self.board.slug,
            'category_slug': self.category.slug,
            'topic_slug': self.topic.slug
        })
        self.assertEqual(absolute_url, reverse_url)


class TestPost(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.board = Board(name='test board')
        self.board.save()
        self.category = Category(board=self.board, name='test category')
        self.category.save()
        self.topic = Topic(user=self.user, category=self.category, name='test topic', message='test topic message')
        self.topic.save()
        self.post = Post(user=self.user, topic=self.topic, message='test post message')
        self.post.save()
        self.msg_old = 'test post message'
        self.msg_new = 'new test message'

    def test_post_message(self):
        self.assertEqual(self.post.message, self.msg_old)

        self.post.message = self.msg_new
        self.post.save()

        self.assertEqual(self.post.message, self.msg_new)

    def test_post_user(self):
        self.assertEqual(self.post.user.username, 'testuser')

        self.post.user = None
        self.post.save

        # change topic.user on_delete
        # self.assertEqual(self.user, None)
        self.assertEqual(self.post.message, self.msg_old)
