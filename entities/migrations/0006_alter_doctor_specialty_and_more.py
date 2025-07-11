# Generated by Django 5.1.7 on 2025-05-14 10:27

import entities.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_alter_analysis_analysis_file_alter_analysis_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(choices=[('ХИР', 'Хирург'), ('ДЕР', 'Дерматолог'), ('ОКУ', 'Окулист'), ('НЕВ', 'Невролог'), ('ТЕР', 'Терапевт')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='specialty',
            field=models.CharField(choices=[('ХИР', 'Хирург'), ('ДЕР', 'Дерматолог'), ('ОКУ', 'Окулист'), ('НЕВ', 'Невролог'), ('ТЕР', 'Терапевт')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[entities.validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[entities.validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
    ]
