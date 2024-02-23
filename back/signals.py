from django.db.models.signals import post_save
from django.dispatch import  receiver
from .models import UserActivity, CustomUser

@receiver(post_save, sender=CustomUser)
def log_user_activity(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(user=instance, action='User created')
    else:
        UserActivity.objects.create(user=instance, action='User updated')