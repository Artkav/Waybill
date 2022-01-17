from django.urls import path
from . import views

app_name = 'waybill'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='regiser'),
    path('logout/', views.logout, name='logout')
]
