from django.urls import path

from .apps import BoardConfig
from . import views

app_name = BoardConfig.label

urlpatterns = [
    path('', view=views.BoardView.as_view(), name='home'),
    path('<slug:board_slug>', view=views.BoardView.as_view(), name='board'),
    path('<slug:board_slug>/<slug:category_slug>',
         view=views.CategoryView.as_view(), name='category'),
    path('<slug:board_slug>/<slug:category_slug>/<slug:topic_slug>',
         view=views.TopicView.as_view(), name='topic'),
    path('<slug:board_slug>/<slug:category_slug>/<slug:topic_slug>',
         view=views.TopicView.as_view(), name='topic_post'),
]
