from django.urls import reverse, resolve
from django.test import Client

from test_plus.test import TestCase


class TestBoardUrls(TestCase):
    """Test URL patterns for board app"""

    def setUp(self):
        self.client = Client()
        self.user = self.make_user()

    def test_index_redirect(self):
        response = self.client.get('', follow=True)

        # test redirect url
        self.assertEqual(response.redirect_chain[0][0], 'board/')
        # test redirect status_code
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_home_reverse(self):
        self.assertEqual(reverse('board:home'), '/board/')

    def test_board_reverse(self):
        self.assertEqual(
            reverse('board:board', kwargs={'board_slug': 'test-board-slug'}),
            '/board/test-board-slug'
        )

    def test_category_reverse(self):
        self.assertEqual(
            reverse('board:category', kwargs={
                'board_slug': 'test-board-slug',
                'category_slug': 'test-category-slug',
            }),
            '/board/test-board-slug/test-category-slug'
        )

    def test_topic_reverse(self):
        self.assertEqual(
            reverse('board:topic', kwargs={
                'board_slug': 'test-board-slug',
                'category_slug': 'test-category-slug',
                'topic_slug': 'test-topic-slug',
            }),
            '/board/test-board-slug/test-category-slug/test-topic-slug'
        )
