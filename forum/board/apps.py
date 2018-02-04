from django.apps import AppConfig


class BoardConfig(AppConfig):
    label = 'board'
    name = 'forum.board'
    verbose_name = "Board"

    def ready(self):
        """Override this to put in:
            Board system checks
            Board signal registration
        """
        pass
