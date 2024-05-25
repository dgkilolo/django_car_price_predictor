from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Make, Model, Vehicle_Images, Vehicle_Data
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn import metrics
import joblib
import pickle
import plotly.express as px

# Create your views here.

# @login_required(login_url='/login')
def home(request):
    car_details = Vehicle_Images.objects.all().order_by('?')[:30]
    return render(request, 'magariPredictor/index.html', {'car_details': car_details})

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
    # read the data from the csv file
    df = pd.read_csv('vehicle_data.csv')

    # sort the data in the csv file in alphabetical order
    df = df.sort_values(by=['Make', 'Model'])

    # get unique vehicle makes from the csv file
    typesOfMake = df['Make'].unique()

    # create a dictionary to map the typesOfCars to numbers
    mapping_makes = {}
    for car_make in typesOfMake:
        mapping_makes[car_make] = typesOfMake.tolist().index(car_make)

    # # # Encoding Vehicle Makes
    df['Make'] = df['Make'].map(mapping_makes)

    # create a dictionary to map the types of Models to numbers
    types_of_models = df['Model'].unique()
    mapping_models = {}
    for car_model in types_of_models:
        mapping_models[car_model] = types_of_models.tolist().index(car_model)
    
    # Encoding vehilce models:
    df['Model'] = df['Model'].map(mapping_models)


    # result = Make.objects.all()
    # model_results = Model.objects.all()
    return render(request, 'magariPredictor/car_details.html', {'showmodel': mapping_models, 'showmake': mapping_makes})

def predict(request):
    model = pd.read_pickle('car_model2.pickle')

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

    # # read the data from the csv file
    df = pd.read_csv('vehicle_data.csv')

    # # sort the data in the csv file in alphabetical order
    df = df.sort_values(by=['Make', 'Model'])

    # # get unique vehicle makes from the csv file
    typesOfMake = df['Make'].unique()

    # # create a dictionary to map the typesOfCars to numbers
    mapping_makes = {}
    for car_make in typesOfMake:
        mapping_makes[typesOfMake.tolist().index(car_make)] = car_make

    # # create a dictionary to map the types of Models to numbers
    types_of_models = df['Model'].unique()
    mapping_models = {}
    for car_model in types_of_models:
        mapping_models[types_of_models.tolist().index(car_model)] = car_model
        
    make = mapping_makes[int(Make)]

    vmodel = mapping_models[int(Model)]

    price_variation_range = 200000

    vehicle_image_results = Vehicle_Images.objects.filter(make=make, model=vmodel, price__gte=predictedPrice-price_variation_range, price__lte=predictedPrice+price_variation_range)[:3]

    if len(vehicle_image_results) == 3:
        vehicle_image_results1 = vehicle_image_results[0]
        vehicle_image_results2 = vehicle_image_results[1]
        vehicle_image_results3 = vehicle_image_results[2]
    elif len(vehicle_image_results) == 2:
        vehicle_image_results1 = vehicle_image_results[0]
        vehicle_image_results2 = vehicle_image_results[1]
        vehicle_image_results3 = None
    elif len(vehicle_image_results) == 1:
        vehicle_image_results1 = vehicle_image_results[0]
        vehicle_image_results2 = None
        vehicle_image_results3 = None
    else:
        vehicle_image_results1 = None
        vehicle_image_results2 = None
        vehicle_image_results3 = None

    datetime.datetime.now()
    current_year = datetime.datetime.now().year
    yom = current_year - int(Age)

    
    return render(request, 'magariPredictor/predict.html', {'predicted_Price': int(predictedPrice[0]), 'vehicle_images1': vehicle_image_results1, 'vehicle_images2': vehicle_image_results2, 'vehicle_images3': vehicle_image_results3,
                                                            'car_make':make, 'car_model':vmodel, 'car_mileage':Mileage, 'car_engine_size':Engine_Size, 'car_fuel_type':Fuel_Type, 'car_transmission':Transmission, 'car_age':yom}) 


def sell_car(request):
    car_details = Vehicle_Images.objects.all().order_by('-id')[:20]
    return render(request, 'magariPredictor/sell_car.html', {'car_details': car_details})

def save_car(request):
    car_details_count = Vehicle_Images.objects.all().count()
    new_id = car_details_count + 1
    if request.method == 'POST':
        make = request.POST['make']
        model = request.POST['model']
        yom = request.POST['yom']
        mileage = request.POST['mileage']
        engine_size = request.POST['engine_size']
        fuel_type = request.POST['fuel_type']
        transmission = request.POST['transmission']
        price = request.POST['price']
        image_url = request.POST['image_url']

        vehicle = Vehicle_Images(id=new_id, make=make, model=model, yom=yom, mileage=mileage, engine_size=engine_size, fuel_type=fuel_type, transmission=transmission, price=price, image_url=image_url)
        vehicle.save()
        return redirect('sell_car')
    else:
        return render(request, 'magariPredictor/sell_car.html')

def enter_pages(request):
    return render(request, 'magariPredictor/scrape_pages.html')


# scrapes data and add it to the list of vehicles for sale
def scrape_data(request):
    if request.method == 'POST':
        # previous size of the database
        previous_data_size = Vehicle_Data.objects.all().count()
        pages = request.POST['pages']
        pages = int(pages)
        # get the data from the website
        for page in range(1, pages + 1):
            url = f'https://autochek.africa/ke/cars-for-sale?price_high=12000000&page_number={page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # div with vehicle image
            car_image_data = soup.find_all('div', class_='MuiBox-root css-1jke4yk')

            # div with vehicle detatils
            car_data = soup.find_all('div', class_='MuiBox-root css-qym38b')

            car_count = len(car_image_data)

            for i in range(car_count):

                car_details_count = Vehicle_Images.objects.all().count()
                new_id = car_details_count + 1

                car_data_count = Vehicle_Data.objects.all().count()
                new_data_id = car_data_count + 1


                car = car_data[i]
                car_img = car_image_data[i]

                car_make = car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[1]
                car_model = ' '.join(car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[2:])
                car_price = int(car.find('p', class_='MuiTypography-root MuiTypography-body1 css-1bztvjj').text.split(' ')[1].replace(',', ''))
                car_year = car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[0]
                car_mileage = int(car.find_all('span', class_='MuiChip-label MuiChip-labelSmall css-1pjtbja')[1].text.split(' ')[0].replace('K', ''))*1000
                car_fuel_type = ''
                car_transmission = 'Automatic'
                car_engine_size = int(car.find_all('span', class_='MuiChip-label MuiChip-labelSmall css-1pjtbja')[2].text.split(' ')[0].replace('Cc', ''))
                car_image_url = car_img.find('span').noscript.img['src']
                if car_make == 'Toyota' and car_model == 'Land Cruiser':
                    car_fuel_type = 'Diesel'
                elif car_make == 'Toyota' and car_engine_size > 2750 and car_engine_size < 2999:
                    car_fuel_type = 'Diesel'
                elif car_make == 'Toyota' and car_model == 'Hilux':
                    car_fuel_type = 'Diesel'
                elif car_make == 'Mazda' and car_model == 'CX-5' and car_engine_size > 2100:
                    car_fuel_type = 'Diesel'
                elif car_make == 'Mazda' and car_model == 'CX-3' and car_engine_size > 1450:
                    car_fuel_type = 'Diesel'
                elif car_make == 'Mazda' and car_model == 'Demio' and car_engine_size > 1450:
                    car_fuel_type = 'Diesel'
                elif car_make == 'Mazda' and car_engine_size > 2100:
                    car_fuel_type = 'Diesel'
                elif car_make == 'Isuzu':
                    car_fuel_type = 'Diesel'
                elif car_make == 'Nissan' and car_model == 'Navara':
                    car_fuel_type = 'Diesel'
                elif car_make == 'Volvo' and car_engine_size == 2000:
                    car_fuel_type = 'Diesel'
                else:
                    car_fuel_type = 'Petrol'
                
                ## check that the data above is not already in the database
                car_exists2 = Vehicle_Data.objects.filter(make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price).exists()
                if not car_exists2:
                    vehicle_data = Vehicle_Data(id=new_data_id, make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price)
                    vehicle_data.save()
                    print("the car has been saved")
                else:
                    pass
                car_exists = Vehicle_Images.objects.filter(make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price, image_url=car_image_url).exists()
                if not car_exists:
                    vehicle = Vehicle_Images(id=new_id, make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price, image_url=car_image_url)
                    vehicle.save()
                else:
                    pass

                # car_exists2 = Vehicle_Data.objects.filter(make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price).exists()
                # if not car_exists2:
                #     vehicle_data = Vehicle_Data(id=new_id, make=car_make, model=car_model, yom=car_year, mileage=car_mileage, engine_size=car_engine_size, fuel_type=car_fuel_type, transmission=car_transmission, price=car_price)
                #     vehicle_data.save()
                # else:
                #     pass

            # current size of the database
            current_data_size = Vehicle_Data.objects.all().count()                               
        return render(request, 'magariPredictor/scraper_stats.html', {'new_rows': (current_data_size - previous_data_size)})
        # return redirect('train_model')


def train_model(request):
    # get the data from the database
    vehicle_data = Vehicle_Data.objects.all()

    # count number of rows in the data
    data_size = Vehicle_Data.objects.all().count()

    # get the current year using datetime, it should be dynamic
    date_time = datetime.datetime.now()
    current_year = date_time.year

    # write this data to a csv file
    with open('vehicle_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Make', 'Model', 'Mileage', 'Engine_Size', 'Fuel_Type', 'Transmission', 'Age', 'Price'])
        for vehicle in vehicle_data:
            writer.writerow([vehicle.make.capitalize(), vehicle.model, vehicle.mileage, vehicle.engine_size, vehicle.fuel_type.capitalize(), vehicle.transmission.capitalize(), (current_year - vehicle.yom), vehicle.price])

    # read the data from the csv file
    df = pd.read_csv('vehicle_data.csv')

    # sort the data in the csv file in alphabetical order
    df = df.sort_values(by=['Make', 'Model'])

    # # # types of fuel
    mappingTypesOfFuel = {'Petrol':0, 'Diesel':1}
    df['Fuel_Type'] = df['Fuel_Type'].map(mappingTypesOfFuel)
    typesOfFuel = df['Fuel_Type'].unique()

    # get unique vehicle makes from the csv file
    typesOfMake = df['Make'].unique()

    # create a dictionary to map the typesOfCars to numbers
    mapping_makes = {}
    for car_make in typesOfMake:
        mapping_makes[car_make] = typesOfMake.tolist().index(car_make)

    # # # Encoding Vehicle Makes
    df['Make'] = df['Make'].map(mapping_makes)

    # create a dictionary to map the types of Models to numbers
    types_of_models = df['Model'].unique()
    mapping_models = {}
    for car_model in types_of_models:
        mapping_models[car_model] = types_of_models.tolist().index(car_model)
    
    # Encoding vehilce models:
    df['Model'] = df['Model'].map(mapping_models)


    # # # encoding transmission type
    mappingTypesOfTransmission = {'Manual':0, 'Automatic':1}
    df['Transmission'] = df['Transmission'].map(mappingTypesOfTransmission)
    typesOfTransmission = df['Transmission'].unique()

    # Store features and target in X and y
    x = df.drop(['Price'], axis=1)
    y = df['Price']

    # split into trainig and testing data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)

    # model training

    lr = LinearRegression()
    lr.fit(x_train, y_train)

    rf = RandomForestRegressor()
    rf.fit(x_train, y_train)

    xgb = GradientBoostingRegressor()
    xgb.fit(x_train, y_train)

    xg = XGBRegressor()
    xg.fit(x_train, y_train)

    # # prediction on the test data

    y_pred1 = lr.predict(x_test)
    y_pred2 = rf.predict(x_test)
    y_pred3 = xgb.predict(x_test)
    y_pred4 = xg.predict(x_test)

    # # # evaluate performance of the model

    score1 = metrics.r2_score(y_test, y_pred1)
    score2 = metrics.r2_score(y_test, y_pred2)
    score3 = metrics.r2_score(y_test, y_pred3)
    score4 = metrics.r2_score(y_test, y_pred4)

    final_data = pd.DataFrame({'Models':['LR', 'RF', 'XGB', 'XG'], 'R2_Score':[score1, score2, score3, score4]})

    # # # save the best model
    xg = XGBRegressor()
    xg_final = xg.fit(x, y)

    pd.to_pickle(xg_final, 'car_model2.pickle')

    return render(request, 'magariPredictor/model_stats.html', {'xg_score': round(score4 * 100, 2), 'data_size':data_size})
    # return redirect('home')