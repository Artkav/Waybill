from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView


def index(request):
    return render(request, template_name='waybill/index.html', context={})


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'waybill/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        next_page = reverse_lazy('waybill:index')
        return reverse_lazy('waybill:index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'waybill/register.html'
    next_page = reverse_lazy('waybill:index')


def logout_user(request):
    logout(request)
    next_page = reverse_lazy('waybill:index')
    return HttpResponse('Log out')
