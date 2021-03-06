from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .form import CreateUserForm, CreateCarForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError


def index(request):
    return render(request, template_name='waybill/index.html', context={})


class RegisterUser(CreateView):
    form_class = CreateUserForm
    template_name = 'waybill/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('waybill:index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'waybill/login.html'
    next_page = reverse_lazy('waybill:index')


def logout_user(request):
    logout(request)
    return redirect('waybill:index')


class CreateCarView(CreateView):
    form_class = CreateCarForm
    template_name = 'waybill/add_new_car.html'

    def form_valid(self, form):
        form.instance.car_driver = self.request.user
        car = form.save()
        return HttpResponseRedirect(reverse('waybill:car-detail', kwargs={'pk': car.id}))


class CarListView(ListView):
    model = Car
    queryset = Car.objects.order_by('car_model')
    template_name = 'waybill/car_list.html'
    context_object_name = 'cars'


class UserDetailView(DetailView):
    model = UpdateUser
    template_name = 'waybill/car_list.html'
    context_object_name = 'member'


class CarDetailView(DetailView):
    model = Car
    template_name = 'waybill/car_detail.html'
    context_object_name = 'car'


def add_first_data(request, car_id):
    if request.method == 'POST':
        start_mileage = int(request.POST.get('start_mileage'))
        tank_residue = int(request.POST.get('tank_residue'))
        new_fuel = Fuel(refueling=0, start_mileage=start_mileage, end_mileage=start_mileage,
                        tank_residue=tank_residue, car=Car.objects.get(id=car_id))
        new_fuel.save()

        return HttpResponseRedirect(reverse('waybill:car-detail', kwargs={'pk': car_id}))
    return render(request, 'waybill:car-detail', kwargs={'pk': car_id})


def send_email(fuel):
    subject = f'?????????? ?? ?????????????? ???? {fuel.date.strftime("%d.%m.%Y %H:%M")} ???? {fuel.car.car_driver}.'
    message = f'{fuel.car.car_model} {fuel.car.state_number} \n???????????? ?????? ????????????: {fuel.start_mileage}???? \n' \
              f'???????????? ?????? ??????????????????????: {fuel.end_mileage}???? \n???????????????????? ?????????????? {fuel.refueling}?? \n' \
              f'???????????????????? ??????????????: {fuel.end_mileage - fuel.start_mileage}???? \n' \
              f'?????????????? ?????????????? ?? ????????: {fuel.tank_residue}??'
    print(message)
    to_email = fuel.car.car_driver.email_for_report
    print(to_email)
    if message and to_email:
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
            print(f'???????????????????? ???? {to_email}')
        except Exception:
            print('??????-???? ?????????? ???? ??????')


def add_daily_report(request, car_id):
    if request.POST.get('refueling'):
        refueling = float(request.POST.get('refueling'))
    else:
        refueling = 0
    start_mileage = int(request.POST.get('start_mileage'))
    if request.POST.get('end_mileage'):
        if int(request.POST.get('end_mileage')) < start_mileage:
            raise ValidationError('???????????? ?????? ???????????? ???????????? ???????? ???????????? ???????????????? ?????? ????????????')
        end_mileage = int(request.POST.get('end_mileage'))
    else:
        end_mileage = start_mileage

    tank_residue = Car.objects.get(id=car_id).fuels.all().first().tank_residue + refueling - \
                   Car.objects.get(id=car_id).consumption_per_100 * (end_mileage - start_mileage) / 100

    new_fuel = Fuel(refueling=refueling, start_mileage=start_mileage, end_mileage=end_mileage,
                    tank_residue=round(tank_residue, 2), car=Car.objects.get(id=car_id))
    new_fuel.save()
    send_email(new_fuel)
    return HttpResponseRedirect(reverse('waybill:car-detail', kwargs={'pk':car_id}))

