from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Car(models.Model):

    Car_name = models.CharField(max_length=30)
    pic_name = models.TextField()
    picurl = models.ImageField()
    Description = models.CharField(max_length=30)
    date = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.Car_name) + '|' + str(self.pk)


class Client(models.Model):

    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    email = models.EmailField(default='pass@gmail.com')
    phone_number = models.IntegerField()
    date_created = models.DateField()
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return str(self.First_name) + ' ' + str(self.Last_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # Add other fields as needed for your user profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

