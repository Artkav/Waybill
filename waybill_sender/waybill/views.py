from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .form import CreateUserForm, CreateCarForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *


def index(request):
    return render(request, template_name='waybill/index.html', context={})


class RegisterUser(CreateView):
    form_class = CreateUserForm
    template_name = 'waybill/register_login.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('waybill:index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'waybill/register_login.html'
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
    model = User
    template_name = 'waybill/car_list.html'
    context_object_name = 'member'


class CarDetailView(DetailView):
    model = Car
    template_name = 'waybill/car_detail.html'
    context_object_name = 'car'


def add_daily_report(request, car_id):
    refueling = int(request.POST.get('refueling'))
    tank_residue = float(request.POST.get('tank_residue'))
    start_mileage = int(request.POST.get('start_mileage'))
    end_mileage = int(request.POST.get('end_mileage'))
    new_fuel = Fuel(refueling=refueling, start_mileage=start_mileage, end_mileage=end_mileage,
                    tank_residue=tank_residue, car=Car.objects.get(id=car_id))
    new_fuel.save()
    return HttpResponseRedirect(reverse('waybill:car-detail', kwargs={'pk':car_id}))

