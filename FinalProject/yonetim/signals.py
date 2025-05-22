from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Notification

@receiver(post_save, sender=User)
def create_user_profile_and_welcome_notification(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Notification.objects.create(
            user=instance,
            message="👋 Welcome to Tempus Naviga! We're glad you're here."
        )
