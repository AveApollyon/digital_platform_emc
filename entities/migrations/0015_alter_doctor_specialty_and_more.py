# Generated by Django 5.1.7 on 2025-05-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0014_rename_icd10_data_historicalvisit_icd10_diagnosis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(choices=[('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог'), ('ХИР', 'Хирург'), ('ОКУ', 'Окулист'), ('ДЕР', 'Дерматолог')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='specialty',
            field=models.CharField(choices=[('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог'), ('ХИР', 'Хирург'), ('ОКУ', 'Окулист'), ('ДЕР', 'Дерматолог')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
    ]
