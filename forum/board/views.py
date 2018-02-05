from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import Board


class BoardView(TemplateView):
    template_name = 'board/index.html'

    def get(self, request, **kwargs):
        try:
            if kwargs:
                board = Board.objects.prefetch_related(
                    'categories__topics__posts').get(slug=kwargs['board_slug'])
            else:
                board = Board.objects.prefetch_related(
                    'categories__topics__posts').first()
            boards = Board.objects.all()
            categories = board.categories.all()
            context = {'board': board, 'boards': boards,
                       'categories': categories}
            return render(
                request,
                context=context,
                template_name=self.template_name)
        except Board.DoesNotExist:
            return redirect('/404/')


class CategoryView(TemplateView):
    pass


class TopicView(TemplateView):
    pass
