from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from django.urls import reverse


# class ApdateUser(AbstractUser):
#     email_for_reporst = models.EmailField(max_length=256, blank=True, null=True)


class Car(models.Model):
    car_model = models.CharField(max_length=128)
    vin_number = models.CharField(max_length=128)
    state_number = models.CharField(max_length=128)
    car_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars') #ApdateUser
    consumption_per_100 = models.FloatField(default=8.0)

    def url(self):
        return reverse('waybill:car-detail', kwargs={'pk': self.id})


class Fuel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='fuels')
    date = models.DateTimeField(default=datetime.datetime.now)
    tank_residue = models.FloatField()
    refueling = models.FloatField(default=0, null=True, blank=True)
    start_mileage = models.PositiveIntegerField()
    end_mileage = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date']

    # def rank_residue_calculating(self):
    def get_absolute_url(self):
        return reverse('waybill:car-detail', kwargs={'pk': self.car.id})






