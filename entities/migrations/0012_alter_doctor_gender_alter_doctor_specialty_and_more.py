# Generated by Django 5.1.7 on 2025-05-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0011_remove_historicalvisit_icd10_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(choices=[('ДЕР', 'Дерматолог'), ('ОКУ', 'Окулист'), ('ХИР', 'Хирург'), ('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='specialty',
            field=models.CharField(choices=[('ДЕР', 'Дерматолог'), ('ОКУ', 'Окулист'), ('ХИР', 'Хирург'), ('ТЕР', 'Терапевт'), ('НЕВ', 'Невролог')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской')], default='М', max_length=1, verbose_name='Пол'),
        ),
    ]
