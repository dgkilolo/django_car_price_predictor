from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('predict', views.predict, name='predict'),
    path('car_details', views.car_details, name='car_details')
]