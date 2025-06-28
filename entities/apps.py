from django.apps import AppConfig
from django.db.models.signals import post_migrate

class EntitiesConfig(AppConfig):
    name = 'entities'

    def ready(self):
        post_migrate.connect(add_default_symptoms, sender=self)

def add_default_symptoms(sender, **kwargs):
    from .models import Symptom

    default_symptoms = [
        "Головная боль",
        "Температура",
        "Кашель",
        "Одышка",
        "Слабость",
        "Боль в животе",
    ]

    print("Начинаем добавление симптомов в базу данных...")

    for symptom_name in default_symptoms:
        symptom, created = Symptom.objects.get_or_create(name=symptom_name)
        # if created:
        #     print(f"Симптом '{symptom_name}' добавлен в базу данных.")
        # else:
        #     print(f"Симптом '{symptom_name}' уже существует в базе данных.")
