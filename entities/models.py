import random
from django.contrib.auth.models import User, Group, Permission
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from entities.validators import *
from simple_history.models import HistoricalRecords


GENDERS = {
    ('М', 'Мужской'),
    ('Ж', 'Женский'),
}

SPECIALTIES = {
    ('ТЕР', 'Терапевт'),
    ('НЕВ', 'Невролог'),
    ('ОКУ', 'Окулист'),
    ('ДЕР', 'Дерматолог'),
    ('ХИР', 'Хирург'),
}

SYMPTOMS_LIST = [
    ("Головная боль", "Головная боль"),
    ("Лихорадка", "Лихорадка"),
    ("Кашель", "Кашель"),
    ("Тошнота", "Тошнота"),
    ("Боль в животе", "Боль в животе"),
    ("Слабость", "Слабость"),
    ("Одышка", "Одышка"),
    ("Потеря аппетита", "Потеря аппетита"),
    ("Головокружение", "Головокружение"),
]
class Patient(models.Model):
    history = HistoricalRecords()

    first_name = models.CharField(max_length=20, verbose_name='Имя', validators=[validate_russian_name])
    last_name = models.CharField(max_length=40, verbose_name='Фамилия', validators=[validate_russian_name])
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', validators=[validate_russian_name])
    date_of_birth = models.DateField(verbose_name='Дата рождения', validators=[validate_date_of_birth])
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', validators=[validate_phone_number])
    email = models.CharField(max_length=50, verbose_name='Электронная почта', validators=[validate_email])
    gender = models.CharField(choices=GENDERS, max_length=1, default='М', verbose_name='Пол')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True)

    # Новые поля
    snils = models.CharField(max_length=11, blank=True, null=True, validators=[validate_snils], verbose_name='СНИЛС пациента')
    inn = models.CharField(max_length=12, blank=True, null=True, validators=[validate_inn], verbose_name='ИНН пациента')
    place_of_birth = models.CharField(max_length=100, blank=True, null=True, validators=[validate_russian_text], verbose_name='Место рождения')
    id_document_type = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Документ, удостоверяющий личность пациента')
    id_document_series_and_number = models.CharField(max_length=20, blank=True, null=True, validators=[validate_document_series_and_number], verbose_name='Серия и номер документа')
    id_document_issued_by = models.CharField(max_length=100, blank=True, null=True, validators=[validate_russian_text], verbose_name='Кем выдан документ')
    id_document_issue_date = models.DateField(blank=True, null=True, validators=[validate_issue_date], verbose_name='Дата выдачи документа')
    race = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Расовая принадлежность')
    marital_status = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Семейное положение')
    number_of_children = models.IntegerField(blank=True, null=True, validators=[validate_number_of_children], verbose_name='Количество детей')
    education_level = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Уровень образования')
    workplace = models.CharField(max_length=100, blank=True, null=True, validators=[validate_russian_text], verbose_name='Место работы')
    position = models.CharField(max_length=100, blank=True, null=True, validators=[validate_russian_text], verbose_name='Должность')
    job_type = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Характер труда')
    social_professional_group = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Социально-профессиональная группа пациента')
    insurance_company = models.CharField(max_length=100, blank=True, null=True, validators=[validate_russian_text], verbose_name='Страховая компания')
    oms_policy_type = models.CharField(max_length=50, blank=True, null=True, validators=[validate_russian_text], verbose_name='Тип полиса ОМС')
    oms_policy_series = models.CharField(max_length=10, blank=True, null=True, validators=[validate_oms_policy_series], verbose_name='Серия полиса ОМС')
    oms_policy_number = models.CharField(max_length=20, blank=True, null=True, validators=[validate_oms_policy_number], verbose_name='Номер полиса ОМС')
    oms_policy_issue_date = models.DateField(blank=True, null=True, validators=[validate_issue_date], verbose_name='Дата выдачи ОМС')

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_username(self):
        username = f"{slugify(self.first_name)}{slugify(self.last_name)}"
        if User.objects.filter(username=username).exists():
            username += str(random.randint(1, 99))
        return username

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @classmethod
    def count_patients(cls):
        return cls.objects.count()

    @classmethod
    def patients_by_age_group(cls):
        from collections import Counter
        age_groups = {
            'age_0_18': 0,
            'age_19_30': 0,
            'age_31_50': 0,
            'age_51_plus': 0,
        }
        for patient in cls.objects.all():
            age = patient.age
            if age <= 18:
                age_groups['age_0_18'] += 1
            elif 19 <= age <= 30:
                age_groups['age_19_30'] += 1
            elif 31 <= age <= 50:
                age_groups['age_31_50'] += 1
            else:
                age_groups['age_51_plus'] += 1
        return age_groups

    @classmethod
    def count_patients_by_gender(cls):
        gender_count = {'М': 0, 'Ж': 0}
        for patient in cls.objects.all():
            gender_count[patient.gender] += 1
        return gender_count



class Doctor(models.Model):
    history = HistoricalRecords()
    first_name = models.CharField(max_length=20, verbose_name='Имя', validators=[validate_russian_name])
    last_name = models.CharField(max_length=40, verbose_name='Фамилия', validators=[validate_russian_name])
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', validators=[validate_russian_name])
    date_of_birth = models.DateField(verbose_name='Дата рождения', validators=[validate_date_of_birth])
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона', validators=[validate_phone_number])
    email = models.CharField(max_length=50, verbose_name='Электронная почта', validators=[validate_email])
    gender = models.CharField(choices=GENDERS, max_length=1, default='М', verbose_name='Пол')
    specialty = models.CharField(choices=SPECIALTIES, max_length=3, default='TER', verbose_name='Специальность')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_username(self):
        username = f"{slugify(self.first_name)}{slugify(self.last_name)}"
        if User.objects.filter(username=username).exists():
            username += str(random.randint(1, 99))
        return username


def create_user(sender, instance, created, **kwargs):
    if created:
        username = get_random_string(length=10)
        password = get_random_string(length=16, allowed_chars='1234567890')
        user, _ = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()
        if isinstance(instance, Patient):
            user.groups.clear()
            user.user_permissions.clear()
            group, created = Group.objects.get_or_create(name='Patients')
            user.groups.add(group)
        elif isinstance(instance, Doctor):
            user.groups.clear()
            user.user_permissions.clear()
            group, created = Group.objects.get_or_create(name='Doctors')
            user.groups.add(group)
            permission, created = Permission.objects.get_or_create(codename='doctor_permission')
            user.user_permissions.add(permission)
        instance.user = user
        instance.save()
        print(username, password)
        send_mail(
            'Ваши входные данные для сервиса электронных мед. карт',
            f'Ваш логин: {username}\nВаш пароль: {password}',
            'd-makhmutov@stud.kpfu.ru',
            [instance.email],
            fail_silently=False,
        )

class Symptom(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    history = HistoricalRecords()
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, verbose_name='Врач', on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom, related_name="visits", blank=True)
    examination = models.TextField(verbose_name='Физический осмотр', validators=[validate_russian_text])
    icd10_diagnosis = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Диагноз по МКБ-10",
        default=list
    )
    consultation = models.BooleanField(default=True, verbose_name="Консультация?")
    visit_date = models.DateTimeField(verbose_name="Дата посещения", validators=[validate_date_time_of_visit])
    prescriptions = models.TextField(verbose_name="Рецепт", validators=[validate_russian_text])

class Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="analyses", verbose_name="Пациент")
    test_name = models.CharField(max_length=200, verbose_name="Название анализа")
    result = models.TextField(verbose_name="Результат")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="analyses", verbose_name="Врач")
    date = models.DateField(verbose_name="Дата")
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('pending', 'Ожидает'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="Статус")
    analysis_file = models.FileField(upload_to='analyses/', null=True, blank=True, verbose_name="Прикрепленный файл")

    def __str__(self):
        return f"{self.test_name} для {self.patient.first_name} {self.patient.last_name}"

    class Meta:
        ordering = ['-date']


class MedicalCard(models.Model):
    history = HistoricalRecords()
    patient = models.ForeignKey(Patient, verbose_name='Пациент', on_delete=models.CASCADE)
    visits = models.ManyToManyField(Visit, verbose_name='Посещения')
    analyses = models.ManyToManyField(Analysis, verbose_name='Анализы')


def create_medical_card(sender, instance, created, **kwargs):
    if created:
        MedicalCard.objects.create(patient=instance)
