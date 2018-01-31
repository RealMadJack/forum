from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .utils import get_unique_slug


class Board(models.Model):
    name = models.CharField(_('Board name'), blank=True, max_length=255)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Board, self.name)
        super().save()


class Category(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(_('Board category name'), max_length=255)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Category, self.name)
        super().save()


class Topic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_('Topic name'), max_length=255)
    message = models.TextField(_('Topic message'), max_length=1024)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(Topic, self.name)
        super().save()


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    message = models.TextField(_('Topic post'), max_length=512)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
