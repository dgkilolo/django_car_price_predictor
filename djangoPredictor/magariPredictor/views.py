from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Make, Model, Vehicle_Images
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
    result = Make.objects.all()
    model_results = Model.objects.all()
    return render(request, 'magariPredictor/car_details.html', {'showmodel': model_results})

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

    # use the vehicle data to query the database
    mappingMakesOfVehicles = {'Audi':0, 'BMW':1, 'Daihatsu':2, 'FAW':3, 'Ford':4, 'Honda':5, 'Hyundai':6, 'Isuzu':7, 'Jaguar':8,
                          'Jeep':9, 'Land Rover':10, 'Lexus':11, 'LEXUS':12, 'Mazda':13, 'Mercedes-Benz':14, 'Mini':15,
                         'Mitsubishi':16, 'Nissan':17, 'Peugeot':18, 'Porsche':19, 'Renault':20, 'Subaru':21, 'Suzuki':22,
                         'TATA':23, 'Toyota':24, 'Volkswagen':25, 'Volvo':26}
    
    make = list(mappingMakesOfVehicles.keys())[list(mappingMakesOfVehicles.values()).index(int(Make))]

    mappingModelsofVehicles = {'A3':0, 'A4':1, 'A5':2, 'A6':3, 'A8':4, 'Q2':5, 'Q3':6, 'Q5':7, 'Q7':8, 'SQ5':9, '116':10, '118':11, '120':12, '218':13, '3 Series':14, '5 Series':15, '730i':16, 'M5':17, 'X1':18, 'X3':19, 'X4':20, 'X5':21, 'X6':22, 'Boon':23, 'Cast Activa':24, 'Hijet':25, 'Mira':26, 'Move':27, 'CA4256':28, 'Escape':29, 'Everest':30, 'Ranger':31, 'CR-V':32, 'Fit':33, 'Freed':34, 'Grace':35, 'Insight':36, 'N-wagon':37, 'Odyssey':38, 'Stepwagon':39, 'Stream':40, 'Vezel':41, 'Santa Fe':42, 'D-Max':43, 'XF':44, 'Compass':45, 'Grand Cherokee':46, 'Discovery 3':47, 'Discovery 4':48, 'Range Rover':49, 'Range Rover Evoque':50, 'Range Rover Sport':51, 'LX 570':52, 'NX':53, 'Rx':54, 'Atenza':55, 'Axela':56, 'Bongo':57, 'Carol':58, 'CX-3':59, 'CX-5':60, 'Demio':61, 'Flair':62, 'Premacy':63, 'A 180':64, 'C 180':65, 'C 200':66, 'E 200':67, 'E 300':68, 'E 400':69, 'E250':70, 'GL 500':71, 'GLA':72, 'GLA 180':73, 'GLA 200':74, 'GLA 250':75, 'GLC 200':76, 'GLC 250':77, 'GLC 350':78, 'GLE':79, 'GLE 250':80, 'GLE 350':81,
               'GLE 43 AMG':82, 'M-Class':83, 'S 300':84, 'S 350':85, 'S 400':86, 'S 550':87, 'Cooper':88, 'Colt':89, 'Delica':90, 'Eclipse':91, 'EK wagon':92, 'evolution':93, 'Fuso Canter':94, 'Galant':95, 'Gk wagon':96, 'L200':97, 'Lancer':98, 'Mirage':99, 'Outlander':100, 'Pajero':101, 'ralliart':102, 'RVR':103, 'Shogun':104, 'Space Wagon':105, 'AD van':106, 'Bluebird':107, 'Caravan':108, 'Cube':109, 'Dayz':110, 'Dualis':111, 'Elgrand':112, 'Fuga':113, 'Juke':114, 'Lafesta':115, 'Latio':116, 'March':117, 'Navara':118, 'Note':119, 'NP 300':120, 'NP200':121, 'NV200':122, 'NV350':123, 'Patrol':124, 'Serena':125, 'Skyline':126, 'Sunny':127, 'Sylphy':128, 'Teana':129, 'Tiida':130, 'Vanette':131, 'Wingroad':132, 'X- trail':133, '208':134, '308':135, '405':136, 'Cayenne':137, 'Macan':138, 'Panamera':139, 'Kadjar':140, 'Kwid':141, 'Forester':142, 'G4':143, 'Impreza':144, 'Legacy':145, 'Levorg':146, 'Outback':147, 'Trezia':148, 'WRX STI':149, 'XV':150, 'Alto':151, 'Baleno':152, 'Ciaz':153, 'Escudo':154, 'Every':155, 'Grand Vitara':156, 'Jimny GL':157, 'Maruti':158, 'S Cross':159, 'Solio':160, 'Spacia':161, 'Swift':162, 'Wagon R':163, 'SUPER ACE':164, 'Allion':165, 'Alphard':166, 'Aqua':167, 'Auris':168, 'Avensis':169, 'Axio':170, 'Belta':171, 'C-HR':172, 'Caldina':173, 'Camry':174, 'Coaster':175, 'Corolla':176, 'Corolla 110':177, 'Corona':178, 'Crown':179, 'Dyna':180, 'esquire':181, 'Estima':182, 'Fielder':183, 'Fj Cruiser':184, 'Fortuner':185, 'GT86':186, 'Harrier':187, 'Hiace':188, 'Hilux':189, 'Hilux Revo':190, 'Hilux vigo':191, 'Ipsum':192, 'Isis':193, 'Ist':194, 'Kluger':195, 'Land Cruiser Prado':196, 'Land Cruiser V8':197, 'Landcruiser  V8':198, 'Landcruiser Prado':199, 'Landcruiser prado TX':200, 'Landcruiser prado TX.L':201, 'Landcruiser prado TZ':202, 'Landcruiser prado TZ.L':203, 'Landcruiser TX.G':204, 'Landcruiser TZ.G':205, 'Landcruiser VX':206, 'Landcruiser Vx V8':207, 'Landcruiser vx.I':208, 'Landcruiser ZX':209, 'Lexus 270':210, 'Lexus RX 350h':211, 'Lexus RX 450h':212, 'Lite-Ace':213, 'Mark II':214, 'Mark X':215, 'Noah':216, 'NZE':217, 'Passo':218, 'Passo Moda':219, 'PIXIS':220, 'Platz':221, 'Porte':222, 'Premio':223, 'Prius':224, 'Probox':225, 'Ractis':226, 'Raum':227, 'RAV 4':228, 'Rumion':229,
               'Rush':230, 'sai hybrid':231, 'Sienna':232, 'Spacio':233, 'Spade':234, 'Succeed':235, 'Sueed':236, 'Surf':237, 'Town Ace':238, 'Toyoace':239, 'Vanguard':240, 'Vellfire':241, 'Verso':242, 'Vitz':243, 'Voxy':244, 'Wish':245, 'Amarok':246, 'Beetle':247, 'Golf':248, 'GTI':249, 'Jetta Gli':250, 'Passat':251, 'Polo':252, 'Tiguan':253, 'Touareg':254, 'Touran':255, 'UP':256, 'S60':257, 'V40':258, 'V70':259, 'XC40':260, 'XC60':261, 'XC70':262, 'XC90':263}

    vmodel = list(mappingModelsofVehicles.keys())[list(mappingModelsofVehicles.values()).index(int(Model))]

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

    
    return render(request, 'magariPredictor/predict.html', {'predicted_Price': predictedPrice[0], 'vehicle_images1': vehicle_image_results1, 'vehicle_images2': vehicle_image_results2, 'vehicle_images3': vehicle_image_results3, 'car_make':make, 'car_model':vmodel}) 

