from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import Board


class BoardView(TemplateView):
    template_name = 'board/index.html'

    def get(self, request, **kwargs):
        if kwargs:
            try:
                board = Board.objects.get(slug=kwargs['board_slug'])
                categories = board.categories.all()
                context = {'board': board, 'categories': categories}
                return render(request, context=context, template_name=self.template_name)
            except Board.DoesNotExist:
                return redirect('/404/')

        board = Board.objects.first()
        context = {'board': board}
        return render(request, context=context, template_name=self.template_name)


class CategoryView(TemplateView):
    pass


class TopicView(TemplateView):
    pass
