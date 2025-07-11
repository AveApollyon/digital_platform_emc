# Generated by Django 5.1.7 on 2025-05-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0013_alter_doctor_specialty_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalvisit',
            old_name='icd10_data',
            new_name='icd10_diagnosis',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='icd10_data',
            new_name='icd10_diagnosis',
        ),
        migrations.RemoveField(
            model_name='historicalvisit',
            name='diagnosis',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='diagnosis',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(choices=[('НЕВ', 'Невролог'), ('ДЕР', 'Дерматолог'), ('ТЕР', 'Терапевт'), ('ХИР', 'Хирург'), ('ОКУ', 'Окулист')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='historicaldoctor',
            name='specialty',
            field=models.CharField(choices=[('НЕВ', 'Невролог'), ('ДЕР', 'Дерматолог'), ('ТЕР', 'Терапевт'), ('ХИР', 'Хирург'), ('ОКУ', 'Окулист')], default='TER', max_length=3, verbose_name='Специальность'),
        ),
    ]
