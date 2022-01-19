from django.urls import path
from . import views

app_name = 'waybill'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('add_new_car/', views.add_car, name='create-car'),
    path('add_car_with_CreateView', views.AddNewCar.as_view(), name='add-car'),
]
