from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(default='pass@gmail.com')
    phone_number = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return str(self.First_name) + ' ' + str(self.Last_name)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # Add other fields as needed for your user profile

    def __str__(self):
        return f"Profile for {self.user}"


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            CustomerProfile.objects.create(user=instance)
            logger.debug(f"Profile created for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'customer_profile'):
            instance.customer_profile.save()
            logger.debug(f"Customer profile saved for user: {instance.username}")
    except Exception as e:
        logger.error(f"Error saving profile for user {instance.username}: {e}")
