from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .form import CreateUserForm, CreateCarForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


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
    template_name = 'waybill/register.html'
    next_page = reverse_lazy('waybill:index')


def logout_user(request):
    logout(request)
    return redirect('waybill:index')


def add_car(request):
    return render(request, template_name='waybill/add_new_car.html', context={})


class AddNewCar(LoginRequiredMixin, CreateView):
    form_class = CreateCarForm
    template_name = 'waybill/add_new_car.html'
    success_url = reverse_lazy('waybill:index')

    def form_valid(self, form):
        form.instance.car_driver = self.request.user
        return super().form_valid(form)
    #
    # def form_valid(self, form):
    #     car = form.save()
    #     return redirect('waybill:index')


