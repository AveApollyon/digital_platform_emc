import json

from django import forms
from django.contrib.auth.models import User, Group
from django.forms import DateInput, DateTimeInput
from entities.models import Visit, Patient, Doctor, Symptom, Analysis
from entities.validators import *
from django_select2.forms import Select2MultipleWidget, Select2Widget

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(validators=[validate_russian_name], label='Имя')
    last_name = forms.CharField(validators=[validate_russian_name], label='Фамилия')
    middle_name = forms.CharField(validators=[validate_russian_name], label='Отчество')
    date_of_birth = forms.DateField(validators=[validate_date_of_birth], label='Дата рождения')
    phone_number = forms.CharField(validators=[validate_phone_number], label='Номер телефона')
    email = forms.EmailField(validators=[validate_email], label='Электронная почта', error_messages={'invalid': 'Введите правильный адрес электронной почты'}),
    username = forms.CharField(required=False, label="Логин (если имеется)")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Пароль (если имеется)")

    # Новые поля
    snils = forms.CharField(max_length=11, required=False, label='СНИЛС пациента')
    inn = forms.CharField(max_length=12, required=False, label='ИНН пациента')
    place_of_birth = forms.CharField(max_length=100, required=False, label='Место рождения')
    id_document_type = forms.CharField(max_length=50, required=False, label='Документ, удостоверяющий личность пациента')
    id_document_series_and_number = forms.CharField(max_length=20, required=False, label='Серия и номер документа')
    id_document_issued_by = forms.CharField(max_length=100, required=False, label='Кем выдан документ')
    id_document_issue_date = forms.DateField(required=False, label='Дата выдачи документа')
    race = forms.CharField(max_length=50, required=False, label='Расовая принадлежность')
    marital_status = forms.CharField(max_length=50, required=False, label='Семейное положение')
    number_of_children = forms.IntegerField(required=False, label='Количество детей')
    education_level = forms.CharField(max_length=50, required=False, label='Уровень образования')
    workplace = forms.CharField(max_length=100, required=False, label='Место работы')
    position = forms.CharField(max_length=100, required=False, label='Должность')
    job_type = forms.CharField(max_length=50, required=False, label='Характер труда')
    harmful_factors = forms.BooleanField(required=False, label='Наличие вредных и (или) опасных производственных факторов')
    social_professional_group = forms.CharField(max_length=50, required=False, label='Социально-профессиональная группа пациента')
    oms_appeal = forms.BooleanField(required=False, label='Обращение по ОМС')
    insurance_company = forms.CharField(max_length=100, required=False, label='Страховая компания')
    oms_policy_type = forms.CharField(max_length=50, required=False, label='Тип полиса ОМС')
    oms_policy_series = forms.CharField(max_length=10, required=False, label='Серия полиса ОМС')
    oms_policy_number = forms.CharField(max_length=20, required=False, label='Номер полиса ОМС')
    oms_policy_issue_date = forms.DateField(required=False, label='Дата выдачи ОМС')
    dms_policy = forms.BooleanField(required=False, label='Полис ДМС')
    paid_services_contract = forms.BooleanField(required=False, label='Договор платных медицинских услуг')

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'email', 'phone_number', 'gender',
                  'snils', 'inn', 'place_of_birth', 'id_document_type', 'id_document_series_and_number',
                  'id_document_issued_by', 'id_document_issue_date', 'race', 'marital_status', 'number_of_children',
                  'education_level', 'workplace', 'position', 'job_type', 'harmful_factors', 'social_professional_group',
                  'oms_appeal', 'insurance_company', 'oms_policy_type', 'oms_policy_series', 'oms_policy_number',
                  'oms_policy_issue_date', 'dms_policy', 'paid_services_contract']
        widgets = {
            'date_of_birth': DateInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
            'id_document_issue_date': DateInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
            'oms_policy_issue_date': DateInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    raise ValidationError("Неверный пароль для указанного логина.")
                cleaned_data['user'] = user
                group, created = Group.objects.get_or_create(name='Patients')
                user.groups.add(group)
            except User.DoesNotExist:
                raise ValidationError("Пользователь с таким логином не найден.")

        return cleaned_data



class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(validators=[validate_russian_name], label='Имя')
    last_name = forms.CharField(validators=[validate_russian_name], label='Фамилия')
    middle_name = forms.CharField(validators=[validate_russian_name], label='Отчество')
    date_of_birth = forms.DateField(validators=[validate_date_of_birth], label='Дата рождения')
    phone_number = forms.CharField(validators=[validate_phone_number], label='Номер телефона')
    email = forms.EmailField(validators=[validate_email], label='Электронная почта')

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'phone_number', 'email', 'gender', 'specialty']
        widgets = {
            'date_of_birth': DateInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
        }



class VisitForm(forms.ModelForm):
    examination = forms.CharField(label='Физический осмотр')
    visit_date = forms.DateTimeField(label="Дата посещения", validators=[validate_date_time_of_visit])
    prescriptions = forms.CharField(label="Рецепт")

    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=Select2MultipleWidget(attrs={'data-placeholder': 'Выберите симптомы'}),
        required=False,
        label="Симптомы"
    )

    icd10_diagnosis = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label=""
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icd10_diagnosis'].initial = '[]'

    def clean_icd10_diagnosis(self):
        data = self.data.get('icd10_diagnosis')
        print(f"Raw ICD10 data in clean: {data}")

        if not data or data == '[]':
            return []

        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            raise forms.ValidationError("Неверный формат данных диагноза")

    class Meta:
        model = Visit
        fields = ['patient', 'doctor', 'visit_date', 'consultation',
                'symptoms', 'examination', 'prescriptions', 'icd10_diagnosis']



class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['patient', 'test_name', 'result', 'doctor', 'date', 'status', 'analysis_file']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'result': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()
        self.fields['doctor'].queryset = Doctor.objects.all()
