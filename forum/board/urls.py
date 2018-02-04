from django.urls import path

from .apps import BoardConfig
from . import views

app_name = BoardConfig.label

urlpatterns = [
    path('', view=views.BoardView.as_view(), name='home'),
    path('<slug:board_slug>', view=views.BoardView.as_view(), name='board'),
]
