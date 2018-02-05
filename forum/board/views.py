from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from .models import Board, Category, Topic, Post
from .forms import TopicForm


class BoardView(TemplateView):
    template_name = 'board/index.html'

    def get(self, request, *args, **kwargs):
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
    template_name = 'board/category.html'

    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.select_related().prefetch_related(
                'topics').get(slug=kwargs['category_slug'])
            topics = category.topics.all()
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
            topic = Topic.objects.select_related().get(
                slug=kwargs['topic_slug'])
            posts = topic.posts.all()
            topic_slug = topic.slug
            category_slug = topic.category.slug
            board_slug = topic.category.board.slug
            context = {
                'topic': topic,
                'posts': posts,
                'form': self.form,
                'board_slug': board_slug,
                'topic_slug': topic_slug,
                'category_slug': category_slug,
            }
            return render(request, context=context, template_name=self.template_name)
        except Topic.DoesNotExist:
            return redirect('/404/')

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                User = get_user_model()
                username = request.user.get_username()
                message = form.cleaned_data['message']

                topic = Topic.objects.get(
                    slug=kwargs['topic_slug'])
                user = User.objects.get(username=username)

                post = Post(
                    topic=topic,
                    user=user,
                    message=message)
                post.save()

                return redirect(topic)
            else:
                return redirect('/403/')
