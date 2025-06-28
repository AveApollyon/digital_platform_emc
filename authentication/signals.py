from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User, Permission
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_to_guests(sender, instance, created, **kwargs):
    if created:
        user_groups = instance.groups.values_list('name', flat=True)
        if 'Doctors' not in user_groups or 'Patients' not in user_groups:
            group, created = Group.objects.get_or_create(name='Guests')
            instance.groups.add(group)
