from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Author


@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    """
    Automatically create an Author profile when a new User is created.
    """
    if created:
        Author.objects.create(user=instance)
