from django.db import models

# Create your models here.


class Dates(models.Model):

    Scheduled_date = models.DateField(unique=True)
