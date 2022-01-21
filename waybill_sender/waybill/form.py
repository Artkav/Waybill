from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = UpdateUser
        fields = ['username', 'email', 'password1', 'password2', 'email_for_report']


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_model', 'vin_number', 'state_number', 'consumption_per_100']

    def clean_vin_number(self):
        vin = self.cleaned_data['vin_number']
        if len(vin) != 17:
            raise ValidationError('Vin должен состоять из 17 символов')
        return vin
