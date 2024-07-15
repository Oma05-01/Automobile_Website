# forms.py
from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['Car_name', 'pic_name', 'picurl', 'Description', 'Available_for_testing', 'date']
        widgets = {
            'Available_for_testing': forms.RadioSelect(choices=Car.AVAILABILITY_CHOICES),
        }
