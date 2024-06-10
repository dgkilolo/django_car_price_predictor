from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('predict', views.predict, name='predict'),
    path('car_details', views.car_details, name='car_details'),
    path('sell_car', views.sell_car, name='sell_car'),
    path('save_car', views.save_car, name='save_car'),
    path('enter_pages', views.enter_pages, name='enter_pages'),
    path('scrape_data', views.scrape_data, name='scrape_data'),
    path('train_model', views.train_model, name='train_model'),
    path('ajax/get_car_models', views.get_car_models, name='ajax_get_car_models'),
]