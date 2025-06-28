import random

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from entities.models import Patient, User, Doctor, Symptom, Visit, Analysis
from datetime import date, datetime
from django.utils.text import slugify


class PatientModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')

        self.patient = Patient.objects.create(
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
            date_of_birth=date(1980, 1, 1),
            phone_number="89872669093",
            email="ivanov@example.com",
            gender="М",
            user=self.user
        )

    def test_get_username(self):
        expected_username = f"{slugify(self.patient.first_name)}{slugify(self.patient.last_name)}"
        self.assertEqual(self.patient.get_username(), expected_username)

    def test_age_calculation(self):
        today = date.today()
        expected_age = today.year - self.patient.date_of_birth.year - (
                    (today.month, today.day) < (self.patient.date_of_birth.month, self.patient.date_of_birth.day))
        self.assertEqual(self.patient.age, expected_age)

    def test_count_patients(self):
        self.assertEqual(Patient.count_patients(), 1)

    def test_patients_by_age_group(self):
        age_groups = Patient.patients_by_age_group()
        self.assertEqual(age_groups['age_0_18'], 0)
        self.assertEqual(age_groups['age_19_30'], 0)
        self.assertEqual(age_groups['age_31_50'], 1)
        self.assertEqual(age_groups['age_51_plus'], 0)

    def test_count_patients_by_gender(self):
        gender_distribution = Patient.count_patients_by_gender()
        self.assertEqual(gender_distribution['М'], 1)
        self.assertEqual(gender_distribution['Ж'], 0)


class PatientViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='adminpassword')

        content_type = ContentType.objects.get_for_model(Patient)
        permission = Permission.objects.create(
            codename='manager_permission',
            name='Can manage patients',
            content_type=content_type
        )

        self.user.user_permissions.add(permission)

        self.client.login(username='admin', password='adminpassword')

    def test_add_patient_success(self):
        patient_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'date_of_birth': '1990-01-01',
            'phone_number': '89872669093',
            'email': 'damir_02@inbox.ru',
            'gender': 'М',
        }

        response = self.client.post(reverse('add_patient'), patient_data)

        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.first()
        self.assertEqual(patient.first_name, 'Иван')
        self.assertEqual(patient.last_name, 'Иванов')


    def test_add_patient_invalid_email(self):
        patient_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'date_of_birth': '1990-01-01',
            'phone_number': '89872669093',
            'email': 'ivanov@example',
            'gender': 'М',
        }

        response = self.client.post(reverse('add_patient'), patient_data)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Некорректный адрес электронной почты'])


class DoctorModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
            specialty='ТЕР',
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.first_name, 'Иван')
        self.assertEqual(self.doctor.last_name, 'Иванов')
        self.assertEqual(self.doctor.middle_name, 'Иванович')
        self.assertEqual(self.doctor.date_of_birth, date(1980, 1, 1))
        self.assertEqual(self.doctor.phone_number, '89872669093')
        self.assertEqual(self.doctor.email, 'ivanov@example.com')
        self.assertEqual(self.doctor.gender, 'М')
        self.assertEqual(self.doctor.specialty, 'ТЕР')

    def test_str_method(self):
        self.assertEqual(str(self.doctor), 'Иванов Иван Иванович')

    def test_get_username(self):
        username = f"{slugify(self.doctor.first_name)}{slugify(self.doctor.last_name)}"
        if User.objects.filter(username=username).exists():
            username += str(random.randint(1, 99))
        self.assertEqual(self.doctor.get_username(), username)


class DoctorViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_add_doctor(self):
        response = self.client.post(reverse('add_doctor'), {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'date_of_birth': date(1980, 1, 1),
            'phone_number': '89872669093',
            'email': 'ivanov@example.com',
            'gender': 'М',
            'specialty': 'ТЕР',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Doctor.objects.count(), 1)

    def test_delete_doctor(self):
        doctor = Doctor.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
            specialty='ТЕР',
        )
        response = self.client.post(reverse('delete_doctor', args=[doctor.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Doctor.objects.count(), 0)


class VisitModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
        )
        self.doctor = Doctor.objects.create(
            first_name='Петр',
            last_name='Петров',
            middle_name='Петрович',
            date_of_birth=date(1975, 5, 5),
            phone_number='89876543210',
            email='petrov@example.com',
            gender='М',
            specialty='ТЕР',
        )

        self.visit = Visit.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            examination='Общее состояние удовлетворительное',
            diagnosis='Мигрень',
            consultation=True,
            visit_date=datetime.now(),
            prescriptions='Парацетамол 500 мг 3 раза в день',
        )
        self.visit.symptoms.set([Symptom.objects.all()[0], Symptom.objects.all()[1]])

    def test_visit_creation(self):
        self.assertEqual(self.visit.patient, self.patient)
        self.assertEqual(self.visit.doctor, self.doctor)
        self.assertEqual(self.visit.examination, 'Общее состояние удовлетворительное')
        self.assertEqual(self.visit.diagnosis, 'Мигрень')
        self.assertEqual(self.visit.consultation, True)
        self.assertEqual(self.visit.prescriptions, 'Парацетамол 500 мг 3 раза в день')
        self.assertEqual(self.visit.symptoms.count(), 2)


class VisitViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

        self.patient = Patient.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
        )
        self.doctor = Doctor.objects.create(
            first_name='Петр',
            last_name='Петров',
            middle_name='Петрович',
            date_of_birth=date(1975, 5, 5),
            phone_number='89876543210',
            email='petrov@example.com',
            gender='М',
            specialty='ТЕР',
        )
        self.symptom1 = Symptom.objects.get(name='Головная боль')
        self.symptom2 = Symptom.objects.get(name='Температура')
    def test_add_visit_success(self):
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'symptoms': [self.symptom1.id, self.symptom2.id],
            'examination': 'Общее состояние удовлетворительное',
            'diagnosis': 'Мигрень',
            'consultation': True,
            'visit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prescriptions': 'Постельный режим',
        }
        response = self.client.post(reverse('add_visit'), data)
        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        visit = Visit.objects.first()
        self.assertEqual(visit.patient, self.patient)
        self.assertEqual(visit.doctor, self.doctor)
        self.assertEqual(visit.symptoms.count(), 2)

    def test_add_visit_invalid_form(self):
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'symptoms': [self.symptom1.id, self.symptom2.id],
            'examination': '',
            'diagnosis': 'Мигрень',
            'consultation': True,
            'visit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prescriptions': 'Парацетамол 500 мг 3 раза в день',
        }
        response = self.client.post(reverse('add_visit'), data)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('examination', form.errors)
        self.assertEqual(form.errors['examination'], ['Обязательное поле.'])

    def test_delete_visit_success(self):
        visit = Visit.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            examination='Общее состояние удовлетворительное',
            diagnosis='Мигрень',
            consultation=True,
            visit_date=datetime.now(),
            prescriptions='Парацетамол 500 мг 3 раза в день',
        )
        response = self.client.post(reverse('delete_visit', args=[visit.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Visit.objects.count(), 0)


class AnalysisModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
        )
        self.doctor = Doctor.objects.create(
            first_name='Петр',
            last_name='Петров',
            middle_name='Петрович',
            date_of_birth=date(1975, 5, 5),
            phone_number='89876543210',
            email='petrov@example.com',
            gender='М',
            specialty='ТЕР',
        )
        self.analysis_file = SimpleUploadedFile("test_file.txt", b"file content")

    def test_create_analysis(self):
        analysis = Analysis.objects.create(
            patient=self.patient,
            test_name="Общий анализ крови",
            result="Все показатели в норме",
            doctor=self.doctor,
            date="2023-10-01",
            status="completed",
            analysis_file=self.analysis_file
        )

        self.assertEqual(Analysis.objects.count(), 1)
        self.assertEqual(analysis.test_name, "Общий анализ крови")
        self.assertEqual(analysis.result, "Все показатели в норме")
        self.assertEqual(analysis.patient, self.patient)
        self.assertEqual(analysis.doctor, self.doctor)
        self.assertEqual(analysis.status, "completed")

    def test_analysis_str(self):
        analysis = Analysis.objects.create(
            patient=self.patient,
            test_name="Общий анализ крови",
            result="Все показатели в норме",
            doctor=self.doctor,
            date="2023-10-01"
        )
        self.assertEqual(str(analysis), "Общий анализ крови для Иван Иванов")


class AddAnalysisViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="doctor", password="testpassword")
        self.client.login(username="doctor", password="testpassword")

        self.patient = Patient.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1980, 1, 1),
            phone_number='89872669093',
            email='ivanov@example.com',
            gender='М',
        )
        self.doctor = Doctor.objects.create(
            first_name='Петр',
            last_name='Петров',
            middle_name='Петрович',
            date_of_birth=date(1975, 5, 5),
            phone_number='89876543210',
            email='petrov@example.com',
            gender='М',
            specialty='ТЕР',
        )
        self.analysis_file = SimpleUploadedFile("test_file.txt", b"file content")

    def test_add_analysis_success(self):
        data = {
            'patient': self.patient.id,
            'test_name': 'Общий анализ крови',
            'result': 'Все показатели в норме',
            'doctor': self.doctor.id,
            'date': '2023-10-01',
            'status': 'completed',
            'analysis_file': self.analysis_file,
        }

        response = self.client.post(reverse('add_analysis'), data)

        self.assertEqual(Analysis.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

        analysis = Analysis.objects.first()
        self.assertEqual(analysis.test_name, "Общий анализ крови")
        self.assertEqual(analysis.result, "Все показатели в норме")
        self.assertEqual(analysis.patient, self.patient)
        self.assertEqual(analysis.doctor, self.doctor)

    def test_add_analysis_invalid_data(self):
        data = {
            'patient': self.patient.id,
            'result': 'Все показатели в норме',
            'doctor': self.doctor.id,
            'date': '2023-10-01',
            'status': 'completed',
            'analysis_file': self.analysis_file,
        }

        response = self.client.post(reverse('add_analysis'), data)


        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('test_name', form.errors)
        self.assertEqual(form.errors['test_name'], ['Обязательное поле.'])
