from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class RegistryConfig(AppConfig):
    name = 'registry'