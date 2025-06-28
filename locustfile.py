import random
from datetime import date

from locust import HttpUser, task, between
from faker import Faker
from bs4 import BeautifulSoup

fake = Faker('ru_RU')
class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Время между запросами


    @task
    def register_user(self):
        username = fake.user_name()
        email = fake.email()
        password = "TestPassword123"
        response = self.client.get("/authentication/register/")
        csrf_token = response.cookies.get("csrftoken")
        # Отправка POST-запроса на регистрацию
        response = self.client.post("/authentication/register/", {
            "username": "testuser",
            "email": email,
            "password1": password,
            "password2": password,
            "csrfmiddlewaretoken": csrf_token

        })

        # Проверка статуса ответа
        if response.status_code != 302:  # Ожидаем редирект после успешной регистрации
            print(f"Ошибка регистрации: {response.status_code}, {response.text}")

    @task
    def login_user(self):
        # Получаем CSRF-токен для страницы входа
        response = self.client.get("/authentication/login/")
        csrf_token = response.cookies.get("csrftoken")

        # Отправка POST-запроса для входа
        response = self.client.post("/authentication/login/", {
            "username": "testuser",
            "password": "TestPassword123",
            "csrfmiddlewaretoken": csrf_token
        })

        # Проверка статуса ответа
        if response.status_code != 302:  # Ожидаем редирект
            print(f"Ошибка авторизации: {response.status_code}, {response.text}")

    @task
    def create_patient(self):
        # Выполняем вход перед созданием пациента
        self.login_user()

        # Получаем CSRF-токен для страницы добавления пациента
        response = self.client.get("/registry/add_patient/")
        csrf_token = response.cookies.get("csrftoken")

        # Генерация данных для пациента
        patient_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
            "gender": fake.random_element(elements=("M", "F")),
            "address": fake.address(),
            "phone_number": fake.phone_number(),
            "email": fake.email(),
            "csrfmiddlewaretoken": csrf_token
        }

        # Отправка POST-запроса для создания пациента
        response = self.client.post("/registry/add_patient/", patient_data)
        if response.status_code not in [200, 201, 302]:  # Успешный ответ
            print(f"Ошибка создания пациента: {response.status_code}, {response.text}")
