from django.db import models

# Create your models here.


class Admin_(models.Model):

    Scheduled_date = models.DateField(unique=True)
