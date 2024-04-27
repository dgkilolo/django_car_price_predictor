import warnings
warnings.filterwarnings('ignore')
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

# df = pd.read_csv('car_data.csv')
df = pd.read_csv('Combined Data.csv')

# typesOfCars = df['Make'].unique()
# print(typesOfCars)

# typesofModels = df['Model'].unique()
# print(typesofModels)

# display top five rows of data set

# bottom5rows = df.tail()
# print(bottom5rows)

# shape = df.shape
# info = df.info()
# print(shape)
# print(info)

# nullValues = df.isnull().sum()
# dataStatistics = df.describe()
# print(nullValues)
# print(dataStatistics)


# # # add age column
date_time = datetime.datetime.now()
df['Age'] = date_time.year - df['YOM']
df.drop(columns='YOM', inplace=True)
# top5rows = df.head()
# print(top5rows)

# emptyCells = df.isnull().sum()
# print(emptyCells)

dropempty = df.dropna()
# print(dropempty)

# chart for car manufactures
# fig = px.histogram(df, x="Make",
#                   labels = {"Make": "Manufacturer"},
#                   title= "Manufacturer of the car",
#                   color_discrete_sequence=["red"])

# fig.show()

# # # remove outliers

# outliers = sns.boxplot(df['Price'])
# outliersSorted = sorted(df['Price'], reverse=True)
# outliersList = df[~(df['Selling_Price']>=33.0) & (df['Selling_Price']<=35.0)]
# print(outliers)
# print(outliersSorted)
# print(outliersList)


# # # encoding for categorical columns
# # # convert categorical columns to numerical columns

# # # types of fuel
mappingTypesOfFuel = {'Petrol':0, 'Diesel':1}
df['Fuel_Type'] = df['Fuel_Type'].map(mappingTypesOfFuel)
typesOfFuel = df['Fuel_Type'].unique()
# print(f'Fuel: {typesOfFuel}')

# # # Encoding Vehicle Makes
mappingMakesOfVehicles = {'Audi':0, 'BMW':1, 'Daihatsu':2, 'FAW':3, 'Ford':4, 'Honda':5, 'Hyundai':6, 'Isuzu':7, 'Jaguar':8,
                          'Jeep':9, 'Land Rover':10, 'Lexus':11, 'LEXUS':12, 'Mazda':13, 'Mercedes-Benz':14, 'Mini':15,
                         'Mitsubishi':16, 'Nissan':17, 'Peugeot':18, 'Porsche':19, 'Renault':20, 'Subaru':21, 'Suzuki':22,
                         'TATA':23, 'Toyota':24, 'Volkswagen':25, 'Volvo':26}
df['Make'] = df['Make'].map(mappingMakesOfVehicles)
MakesOfVehicles = df['Make'].unique()
# print(f'Make: {MakesOfVehicles}')

# Encoding vehilce models:
mappingModelsofVehicles = {'A3':0, 'A4':1, 'A5':2, 'A6':3, 'A8':4, 'Q2':5, 'Q3':6, 'Q5':7, 'Q7':8, 'SQ5':9, '116':10, '118':11, '120':12, '218':13, '3 Series':14, '5 Series':15, '730i':16, 'M5':17, 'X1':18, 'X3':19, 'X4':20, 'X5':21, 'X6':22, 'Boon':23, 'Cast Activa':24, 'Hijet':25, 'Mira':26, 'Move':27, 'CA4256':28, 'Escape':29, 'Everest':30, 'Ranger':31, 'CR-V':32, 'Fit':33, 'Freed':34, 'Grace':35, 'Insight':36, 'N-wagon':37, 'Odyssey':38, 'Stepwagon':39, 'Stream':40, 'Vezel':41, 'Santa Fe':42, 'D-Max':43, 'XF':44, 'Compass':45, 'Grand Cherokee':46, 'Discovery 3':47, 'Discovery 4':48, 'Range Rover':49, 'Range Rover Evoque':50, 'Range Rover Sport':51, 'LX 570':52, 'NX':53, 'Rx':54, 'Atenza':55, 'Axela':56, 'Bongo':57, 'Carol':58, 'CX-3':59, 'CX-5':60, 'Demio':61, 'Flair':62, 'Premacy':63, 'A 180':64, 'C 180':65, 'C 200':66, 'E 200':67, 'E 300':68, 'E 400':69, 'E250':70, 'GL 500':71, 'GLA':72, 'GLA 180':73, 'GLA 200':74, 'GLA 250':75, 'GLC 200':76, 'GLC 250':77, 'GLC 350':78, 'GLE':79, 'GLE 250':80, 'GLE 350':81,
               'GLE 43 AMG':82, 'M-Class':83, 'S 300':84, 'S 350':85, 'S 400':86, 'S 550':87, 'Cooper':88, 'Colt':89, 'Delica':90, 'Eclipse':91, 'EK wagon':92, 'evolution':93, 'Fuso Canter':94, 'Galant':95, 'Gk wagon':96, 'L200':97, 'Lancer':98, 'Mirage':99, 'Outlander':100, 'Pajero':101, 'ralliart':102, 'RVR':103, 'Shogun':104, 'Space Wagon':105, 'AD van':106, 'Bluebird':107, 'Caravan':108, 'Cube':109, 'Dayz':110, 'Dualis':111, 'Elgrand':112, 'Fuga':113, 'Juke':114, 'Lafesta':115, 'Latio':116, 'March':117, 'Navara':118, 'Note':119, 'NP 300':120, 'NP200':121, 'NV200':122, 'NV350':123, 'Patrol':124, 'Serena':125, 'Skyline':126, 'Sunny':127, 'Sylphy':128, 'Teana':129, 'Tiida':130, 'Vanette':131, 'Wingroad':132, 'X- trail':133, '208':134, '308':135, '405':136, 'Cayenne':137, 'Macan':138, 'Panamera':139, 'Kadjar':140, 'Kwid':141, 'Forester':142, 'G4':143, 'Impreza':144, 'Legacy':145, 'Levorg':146, 'Outback':147, 'Trezia':148, 'WRX STI':149, 'XV':150, 'Alto':151, 'Baleno':152, 'Ciaz':153, 'Escudo':154, 'Every':155, 'Grand Vitara':156, 'Jimny GL':157, 'Maruti':158, 'S Cross':159, 'Solio':160, 'Spacia':161, 'Swift':162, 'Wagon R':163, 'SUPER ACE':164, 'Allion':165, 'Alphard':166, 'Aqua':167, 'Auris':168, 'Avensis':169, 'Axio':170, 'Belta':171, 'C-HR':172, 'Caldina':173, 'Camry':174, 'Coaster':175, 'Corolla':176, 'Corolla 110':177, 'Corona':178, 'Crown':179, 'Dyna':180, 'esquire':181, 'Estima':182, 'Fielder':183, 'Fj Cruiser':184, 'Fortuner':185, 'GT86':186, 'Harrier':187, 'Hiace':188, 'Hilux':189, 'Hilux Revo':190, 'Hilux vigo':191, 'Ipsum':192, 'Isis':193, 'Ist':194, 'Kluger':195, 'Land Cruiser Prado':196, 'Land Cruiser V8':197, 'Landcruiser  V8':198, 'Landcruiser Prado':199, 'Landcruiser prado TX':200, 'Landcruiser prado TX.L':201, 'Landcruiser prado TZ':202, 'Landcruiser prado TZ.L':203, 'Landcruiser TX.G':204, 'Landcruiser TZ.G':205, 'Landcruiser VX':206, 'Landcruiser Vx V8':207, 'Landcruiser vx.I':208, 'Landcruiser ZX':209, 'Lexus 270':210, 'Lexus RX 350h':211, 'Lexus RX 450h':212, 'Lite-Ace':213, 'Mark II':214, 'Mark X':215, 'Noah':216, 'NZE':217, 'Passo':218, 'Passo Moda':219, 'PIXIS':220, 'Platz':221, 'Porte':222, 'Premio':223, 'Prius':224, 'Probox':225, 'Ractis':226, 'Raum':227, 'RAV 4':228, 'Rumion':229,
               'Rush':230, 'sai hybrid':231, 'Sienna':232, 'Spacio':233, 'Spade':234, 'Succeed':235, 'Sueed':236, 'Surf':237, 'Town Ace':238, 'Toyoace':239, 'Vanguard':240, 'Vellfire':241, 'Verso':242, 'Vitz':243, 'Voxy':244, 'Wish':245, 'Amarok':246, 'Beetle':247, 'Golf':248, 'GTI':249, 'Jetta Gli':250, 'Passat':251, 'Polo':252, 'Tiguan':253, 'Touareg':254, 'Touran':255, 'UP':256, 'S60':257, 'V40':258, 'V70':259, 'XC40':260, 'XC60':261, 'XC70':262, 'XC90':263}
df['Model'] = df['Model'].map(mappingModelsofVehicles)
ModelsofVehicles = df['Model'].unique()
# print(f'Models: {len(ModelsofVehicles)}')

# # # encoding seller type
# mappingTypesOfSellers = {'Dealer':0, 'Individual':1}
# df['Seller_Type'] = df['Seller_Type'].map(mappingTypesOfSellers)
# typesOfSellers = df['Seller_Type'].unique()
# # print(typesOfSellers)

# # # encoding transmission type
mappingTypesOfTransmission = {'Manual':0, 'Automatic':1}
df['Transmission'] = df['Transmission'].map(mappingTypesOfTransmission)
typesOfTransmission = df['Transmission'].unique()
# print(f'Transmission: {typesOfTransmission}')


# # Store features and target in X and y
x = df.drop(['Price'], axis=1)
y = df['Price']
# print(x)
# print(y)


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

# print(score1, score2, score3, score4)


final_data = pd.DataFrame({'Models':['LR', 'RF', 'XGB', 'XG'], 'R2_Score':[score1, score2, score3, score4]})

print(final_data)

# save the best model

xg = XGBRegressor()
xg_final = xg.fit(x, y)

pd.to_pickle(xg_final, 'car_model.pickle')


# joblib.dump(xg_final, 'xg_final.pkl')

# model = joblib.load('xg_final.pkl')

# xg_final.save_model('xg_final.json')

# Predict on new data

# create a data frame

# data_new = pd.DataFrame({
#     'Make': [17], # Nissan
#     'Model': [119], # 'Model': 'Note
#     'Mileage': [80360],
#     'Engine_Size': [1200],
#     'Fuel_Type': [0],
#     'Transmission': [0],
#     'Age': [8],
    
# })

# predictedPrice = model.predict(data_new)

# print(f'Predicted Price: Nissan Note: {predictedPrice[0]}Ksh')

# data_new = pd.DataFrame({
#     'Make': [24], # Toyota
#     'Model': [165], # 'Model': 'Allion
#     'Mileage': [80360],
#     'Engine_Size': [1800],
#     'Fuel_Type': [0],
#     'Transmission': [0],
#     'Age': [8],
    
# })

# predictedPrice = model.predict(data_new)


# print(f'Predicted Price: Toyota Allion: {predictedPrice[0]}Ksh')