import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_russian_name(name):
    words = name.split()
    for word in words:
        if not word[0].isupper():
            raise ValidationError("ФИО должны начинаться с заглавных букв")
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', name):
        raise ValidationError("ФИО должно быть на русском языке")


def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError("Некорректный адрес электронной почты")


def validate_date_of_birth(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    if date_of_birth > today:
        raise ValidationError("Дата рождения не может быть в будущем")
    elif age < 18:
        raise ValidationError("Пациент должен был совершеннолетним")
    elif age > 120:
        raise ValidationError("Возраст должен быть меньше 120 лет")


def validate_phone_number(phone_number):
    if not re.match(r'^(\+7|8)[0-9]{10}$', phone_number):
        raise ValidationError("Некорректный номер телефона")


def validate_symptoms(symptoms):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', symptoms):
        raise ValidationError("Описание симптомов должно быть на русском языке")


def validate_examination(examination):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', examination):
        raise ValidationError("Описание осмотра должно быть на русском языке")


def validate_diagnosis(diagnosis):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', diagnosis):
        raise ValidationError("Описание диагноза должно быть на русском языке")


def validate_date_time_of_visit(visit_date):
    current_time = timezone.localtime(timezone.now())
    if timezone.localtime(visit_date) > current_time:
        raise ValidationError("Дата посещения не может быть в будущем")


def validate_prescriptions(prescriptions):
    if not re.match(r'^[А-Яа-яёЁ\s-]+$', prescriptions):
        raise ValidationError("Рецепт должен быть на русском языке")


def validate_snils(value):
    if value and not re.fullmatch(r'\d{11}', value):
        raise ValidationError("СНИЛС должен состоять из 11 цифр")

def validate_inn(value):
    if value and not re.fullmatch(r'\d{12}', value):
        raise ValidationError("ИНН должен состоять из 12 цифр")

def validate_russian_text(value):
    if value and not re.fullmatch(r'^[А-Яа-яёЁ0-9\s.,\-()]+$', value):
        raise ValidationError("Поле должно содержать текст на русском языке")

def validate_document_series_and_number(value):
    if value and not re.fullmatch(r'^[А-Яа-яЁё0-9\s-]+$', value):
        raise ValidationError("Серия и номер документа должны быть на русском языке или цифрами")

def validate_issue_date(value):
    if value and value > date.today():
        raise ValidationError("Дата не может быть в будущем")

def validate_number_of_children(value):
    if value is not None and value < 0:
        raise ValidationError("Количество детей не может быть отрицательным")

def validate_oms_policy_series(value):
    if value and not re.fullmatch(r'\d{4,10}', value):
        raise ValidationError("Серия полиса должна содержать от 4 до 10 цифр")

def validate_oms_policy_number(value):
    if value and not re.fullmatch(r'\d{6,20}', value):
        raise ValidationError("Номер полиса должен содержать от 6 до 20 цифр")
