from django.db import models

# Create your models here.
class Customer(models.Model):

    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    email = models.EmailField(default='pass@gmail.com')
    phone_number = models.IntegerField(max_length=11)
    date_created = models.DateField()

    def __str__(self):
        return str(self.First_name) + ' ' + str(self.Last_name)