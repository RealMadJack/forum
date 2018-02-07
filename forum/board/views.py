from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from .models import Board, Category, Topic, Post
from .forms import TopicForm


class BoardView(TemplateView):
    template_name = 'board/index.html'

    def get(self, request, *args, **kwargs):
        try:
            board = Board.objects.prefetch_related('categories__topics__posts')
            if kwargs:
                board = board.get(slug=kwargs['board_slug'])
            else:
                board = board.first()
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
    template_name = 'board/category.html'

    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.select_related().get(
                slug=kwargs['category_slug'])
            topics = category.topics.prefetch_related('posts').all()
            context = {'category': category, 'topics': topics}
            return render(
                request,
                context=context,
                template_name=self.template_name)
        except Category.DoesNotExist:
            return redirect('/404/')


class TopicView(TemplateView):
    template_name = 'board/topic.html'
    form = TopicForm

    def get(self, request, *args, **kwargs):
        try:
            topic = Topic.objects.select_related().get(slug=kwargs['topic_slug'])
            posts = topic.posts.select_related().all()
            context = {
                'topic': topic,
                'posts': posts,
                'form': self.form,
            }
            return render(request, context=context, template_name=self.template_name)
        except Topic.DoesNotExist:
            return redirect('/404/')

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        topic = get_object_or_404(Topic, slug=kwargs['topic_slug'])

        if form.is_valid():
            if request.user.is_authenticated:
                User = get_user_model()
                username = request.user.get_username()
                message = form.cleaned_data['message']
                user = get_object_or_404(User, username=username)

                post = Post(
                    topic=topic,
                    user=user,
                    message=message)
                post.save()

                return redirect(topic)
            else:
                return redirect('/404/')
        else:
            form = self.form()
        return redirect(topic)
