import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import random
from faker import Faker
from datetime import datetime, timedelta
from entities.models import Analysis, Patient, Doctor
fake = Faker('ru_RU')

patients = list(Patient.objects.all())
doctors = list(Doctor.objects.all())

STATUS_CHOICES = ['in_progress', 'completed', 'pending']

def random_analysis_date():
    now = datetime.now()
    days_back = random.randint(0, 180)
    return now - timedelta(days=days_back)

test_names = [
    "Общий анализ крови",
    "Биохимический анализ крови",
    "Анализ мочи",
    "МРТ",
    "УЗИ",
    "Рентгенография",
    "Гормональный профиль",
    "Анализ на антитела",
    "Коагулограмма",
    "Глюкозотолерантный тест"
]

for _ in range(500):  # создаем 500 анализов
    patient = random.choice(patients)
    doctor = random.choice(doctors)
    test_name = random.choice(test_names)
    result = fake.text(max_nb_chars=200)
    date = random_analysis_date().date()
    status = random.choice(STATUS_CHOICES)

    analysis = Analysis.objects.create(
        patient=patient,
        doctor=doctor,
        test_name=test_name,
        result=result,
        date=date,
        status=status,
        analysis_file=None  # или можно добавить логику для фиктивных файлов, если нужно
    )

    print(f"Анализ #{analysis.id} создан: {test_name} для пациента {patient} врачом {doctor} на дату {date}")
