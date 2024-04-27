from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Car
import pandas as pd
import joblib

# Create your views here.

# @login_required(login_url='/login')
def home(request):
    return render(request, 'magariPredictor/index.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()

    return render(request, 'registration/sign_up.html', {'form': form})

def car_details(request):
    return render(request, 'magariPredictor/car_details.html')

def predict(request):
    model = pd.read_pickle('car_model.pickle')

    Make = request.GET['Make']
    Model = request.GET['Model']
    Mileage = request.GET['Mileage']
    Engine_Size = request.GET['Engine_Size']
    Fuel_Type = request.GET['Fuel_Type']
    Transmission = request.GET['Transmission']
    Age = request.GET['Age']

    data_new = pd.DataFrame({
        'Make': [int(Make)],
        'Model': [int(Model)],
        'Mileage': [int(Mileage)],
        'Engine_Size': [int(Engine_Size)],
        'Fuel_Type': [int(Fuel_Type)],
        'Transmission': [int(Transmission)],
        'Age': [int(Age)]
    })

    predictedPrice = model.predict(data_new)

    return render(request, 'magariPredictor/predict.html', {'predicted_Price': predictedPrice})

