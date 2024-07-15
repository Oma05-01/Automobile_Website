from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
# Create your models here.


class Car(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]

    Car_name = models.CharField(max_length=30)
    pic_name = models.TextField()
    picurl = models.ImageField(upload_to='car_pics/')
    Description = models.CharField(max_length=30)
    Available_for_testing = models.CharField(
        max_length=15,
        choices=AVAILABILITY_CHOICES,
        default='not_available'
    )
    date = models.CharField(max_length=50, default="")
    price = models.IntegerField()
    test_drive_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    test_location = models.TextField()

    def __str__(self):
        return f"{self.Car_name}|{self.pk}"

    # def calculate_test_drive_fee(self):
    #     # Define base price and corresponding fee percentage
    #     base_price_threshold = 100000  # Base threshold price
    #     base_fee_percentage = 0.001  # Base fee percentage per $20,000
    #
    #     if self.price > base_price_threshold:
    #         # Calculate how many times the price exceeds the base threshold
    #         price_multiple = self.price / base_price_threshold
    #         # Set the fee based on the multiple of the base threshold
    #         self.test_drive_fee = self.price * (price_multiple * base_fee_percentage)
    #     else:
    #         # If price is not greater than base threshold, set default fee
    #         self.test_drive_fee = self.price * base_fee_percentage
    #
    # def save(self, *args, **kwargs):
    #     self.calculate_test_drive_fee()
    #     super().save(*args, **kwargs)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(default='pass@gmail.com')
    phone_number = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return str(self.First_name) + ' ' + str(self.Last_name)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
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
            ClientProfile.objects.create(user=instance)
            logger.debug(f"Profile created for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'client_profile'):
            instance.client_profile.save()
            logger.debug(f"Client profile saved for user: {instance.username}")
    except Exception as e:
        logger.error(f"Error saving profile for user {instance.username}: {e}")

