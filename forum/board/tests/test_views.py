from django.urls import reverse
from django.test import RequestFactory, Client
from test_plus.test import TestCase

from ..models import Board, Category, Topic, Post
from ..views import BoardView


class BaseBoardTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.client = Client()
        self.factory = RequestFactory()
        self.board = Board(name='test board')
        self.board.save()
        self.category = Category(board=self.board, name='test category')
        self.category.save()
        self.topic = Topic(user=self.user, category=self.category,
                           name='test topic', message='test topic message')
        self.topic.save()
        self.post = Post(user=self.user, topic=self.topic,
                         message='test post message')
        self.post.save()


class TestBoardView(BaseBoardTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestBoardView, self).setUp()
        self.board_url_valid = reverse(
            'board:board', kwargs={'board_slug': self.board.slug})
        self.board_url_invalid = reverse(
            'board:board', kwargs={'board_slug': 'invalid_slug'})

    def test_get_view_status_code(self):
        request = self.factory.get(self.board_url_valid)
        response = BoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_view_status_code_invalid(self):
        response_client = self.client.get(self.board_url_invalid, follow=True)
        self.assertEqual(response_client.redirect_chain[0][1], 302)
        self.assertEqual(response_client.status_code, 404)


class TestCategoryView(BaseBoardTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestCategoryView, self).setUp()
        self.category_url_valid = reverse('board:category', kwargs={
            'board_slug': self.board.slug,
            'category_slug': self.category.slug,
        })
        self.category_url_invalid = reverse('board:category', kwargs={
            'board_slug': 'invalid_slug',
            'category_slug': 'invalid_slug',
        })

    def test_get_view_status_code(self):
        response_client = self.client.get(self.category_url_valid)
        self.assertEqual(response_client.status_code, 200)

    def test_get_view_status_code_invalid(self):
        response_client = self.client.get(
            self.category_url_invalid, follow=True)
        self.assertEqual(response_client.redirect_chain[0][1], 302)
        self.assertEqual(response_client.status_code, 404)


class TestTopicView(BaseBoardTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestTopicView, self).setUp()
        self.topic_url_valid = reverse('board:topic', kwargs={
            'board_slug': self.board.slug,
            'category_slug': self.category.slug,
            'topic_slug': self.topic.slug,
        })
        self.topic_url_invalid = reverse('board:topic', kwargs={
            'board_slug': 'invalid_slug',
            'category_slug': 'invalid_slug',
            'topic_slug': 'invalid_slug',
        })

    def test_get_view_status_code(self):
        response_client = self.client.get(self.topic_url_valid)
        self.assertEqual(response_client.status_code, 200)

    def test_get_view_status_code_invalid(self):
        response_client = self.client.get(self.topic_url_invalid, follow=True)
        self.assertEqual(response_client.redirect_chain[0][1], 302)
        self.assertEqual(response_client.status_code, 404)

    def test_post_view_valid(self):
        self.client.login(username=self.user.username, password='password')
        response_client = self.client.post(
            self.topic_url_valid, {'message': 'test'},
            follow=True)
        # Redirect chain status_code
        self.assertEqual(response_client.redirect_chain[0][1], 302)
        # Redirect chain url
        self.assertEqual(
            response_client.redirect_chain[0][0], '/board/test-board/test-category/test-topic')
        # Redirected page response status_code
        self.assertEqual(response_client.status_code, 200)

    def test_post_view_invalid_user(self):
        self.client.login(username=self.user.username, password='')
        response_client = self.client.post(
            self.topic_url_valid, {'message': 'test'},
            follow=True)
        # Unknown user redirected to 404
        self.assertEqual(response_client.status_code, 404)

    def test_post_view_invalid_data(self):
        self.client.login(username=self.user.username, password='password')
        response_client = self.client.post(
            self.topic_url_valid, {'message': ''},
            follow=True)
        # Redirect to the same page with errors
        self.assertEqual(response_client.redirect_chain[0][1], 302)
        # Final response_code
        self.assertEqual(response_client.status_code, 200)
