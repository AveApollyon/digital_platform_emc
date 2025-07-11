# Generated by Django 5.1.7 on 2025-05-14 10:27

import django.db.models.deletion
import entities.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0004_alter_doctor_specialty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='analysis_file',
            field=models.FileField(blank=True, null=True, upload_to='analyses/', verbose_name='Прикрепленный файл'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='entities.doctor', verbose_name='Врач'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='entities.patient', verbose_name='Пациент'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='result',
            field=models.TextField(verbose_name='Результат'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='status',
            field=models.CharField(choices=[('in_progress', 'В процессе'), ('completed', 'Завершено'), ('pending', 'Ожидает')], default='in_progress', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='test_name',
            field=models.CharField(max_length=200, verbose_name='Название анализа'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(choices=[('ДЕР', 'Дерматолог'), ('ХИР', 'Хирург'), ('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог'), ('ОКУ', 'Окулист')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='specialty',
            field=models.CharField(choices=[('ДЕР', 'Дерматолог'), ('ХИР', 'Хирург'), ('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог'), ('ОКУ', 'Окулист')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[entities.validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[entities.validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
    ]
