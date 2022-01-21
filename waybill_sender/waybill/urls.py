from django.urls import path
from . import views

app_name = 'waybill'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    # path('add_new_car/', views.add_car, name='create-car'),
    path('add_car_with_CreateView/<int:pk>', views.CreateCarView.as_view(), name='add-car'),
    path('user_car_list/<int:pk>', views.UserDetailView.as_view(), name='car-list'),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('add report/<int:car_id>', views.add_daily_report, name='add-daily-report'),
    path('add first report/<int:car_id>', views.add_first_data, name='add-first-data'),
]
