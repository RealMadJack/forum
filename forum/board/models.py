from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from .utils import get_unique_slug


class Board(TimeStampedModel):
    name = models.CharField(_('Board name'), blank=True, max_length=255)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board:board', kwargs={'board_slug': self.slug})

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Board, self.name)
        super().save()


class Category(TimeStampedModel):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='categories',
        related_query_name='category',
    )
    name = models.CharField(_('Board category name'), max_length=255)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board:category', kwargs={
            'category_slug': self.slug,
            'board_slug': self.board.slug,
        })

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Category, self.name)
        super().save()


class Topic(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='topics',
        related_query_name='topic',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='topics',
        related_query_name='topic',
    )
    name = models.CharField(_('Topic name'), max_length=255)
    message = models.TextField(_('Topic message'), max_length=1024)
    slug = models.SlugField(max_length=155, unique=True)

    @property
    def short_message(self):
        return self.message[:150].strip()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board:topic', kwargs={
            'topic_slug': self.slug,
            'category_slug': self.category.slug,
            'board_slug': self.category.board.slug,
        })

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Topic, self.name)
        super().save()


class Post(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        related_query_name='post',
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='posts',
        related_query_name='post',
    )
    message = models.TextField(_('Topic post'), max_length=512)

    @property
    def short_message(self):
        return self.message[:150].strip()

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
