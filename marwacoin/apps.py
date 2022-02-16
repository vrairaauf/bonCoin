from django.apps import AppConfig


class MarwacoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marwacoin'
    def ready(self):
    	import marwacoin.signals