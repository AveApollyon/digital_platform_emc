from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from .models import Patient, create_medical_card, create_user, MedicalCard, Doctor

@receiver(post_save, sender=Patient)
def create_medical_card_signal(sender, instance, created, **kwargs):
    create_medical_card(sender, instance, created, **kwargs)


@receiver(post_save, sender=Patient)
def create_user_signal(sender, instance, created, **kwargs):
    if created and not instance.user:
        create_user(sender, instance, created, **kwargs)


@receiver(pre_delete, sender=Patient)
@receiver(pre_delete, sender=Doctor)
def delete_user_signal(sender, instance, **kwargs):
    if instance.user and instance.user.pk:
        instance.user.delete()


@receiver(pre_delete, sender=MedicalCard)
def delete_visits_signal(sender, instance, **kwargs):
    instance.visits.clear()
