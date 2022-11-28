import os
import pickle
import statistics
import numpy as np
import pandas as pd

from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

from utils.upload_file import upload_file
from utils.download_file import download_file

def train_model():
    #IMPORT RAW DATA---------------------------------------------------
    df = pd.read_csv(download_file("data/properties.csv", "properties_data_akl.csv"))

    #CLEAN & TRANSFORM RAW DATA----------------------------------------

    z_scores_price = stats.zscore(df['price'])
    abs_z_scores_price = np.abs(z_scores_price) 
    filtered_entries_price = (abs_z_scores_price < 1)
    df = df[filtered_entries_price]
    #Price (float)
    df= df.loc[df['price'] != -1]
    #Surface (float)
    df = df.loc[df['surface'] <= 800]
    df = df.loc[df['surface'] >= 35]
    df = df.loc[df['surface'] != -1]
    #Sub type of property (str)
    df= df.loc[df['subtype_of_property'] != 'APARTMENT_BLOCK']
    df= df.loc[df['subtype_of_property'] != 'MIXED_USE_BUILDING']
    others = ["CHALET", "MANOR_HOUSE", "OTHER_PROPERTY", "CASTLE", "PAVILION"]
    df.loc[df["subtype_of_property"].isin(others), "type_of_property"] = "OTHER"
    #Number of bedrooms (int)
    df = df.loc[df['number_of_bedrooms'] <20]
    df['type_of_property'] = np.where((df['number_of_bedrooms'] > 20), "OTHER", df['type_of_property'])
    df['number_of_bedrooms'] = df['number_of_bedrooms'].replace(-1,0)
    #Zip Code (category)
    df['zip_code_xx'] = df['postal_code'].apply(lambda x : 'be_zip_'+str(x)[:2])
    #Land surface (float)
    df['land_surface'] = [land_surface if land_surface != -1 else garden_surface if garden_surface > 0 else land_surface for garden_surface,land_surface in zip(df['garden_surface'],df['land_surface'])]
    df['land_surface'] = df['land_surface'].replace(-1,0)
    #Garden (0,1)
    df['garden'] = df['garden'].replace(-1,0)
    #Garden surface (float)
    df['garden_surface'] = df['garden_surface'].replace(-1,0)
    df['garden_surface'] = df['garden_surface'].replace(1,0)
    df.loc[(df["garden_surface"] > 2000) & (df['type_of_property'] == 'APARTMENT'),'type_of_property'] = "OTHER"
    #Fully equiped kitchen (int) change later, calculate each value y/n
    df["fully_equipped_kitchen"] = df["fully_equipped_kitchen"].map({"-1.0": 0.5,
                                                                    "1.0": 1,
                                                                    "-1": 0.5, 
                                                                    "1": 1, 
                                                                    "INSTALLED": 0.75, 
                                                                    "SEMI_EQUIPPED": 0.60, 
                                                                    "NOT_INSTALLED": 0.57, 
                                                                    "USA_INSTALLED": 0.85, 
                                                                    "USA_SEMI_EQUIPPED": 0.80, 
                                                                    "USA_UNINSTALLED": 0.75})
    #Swiming pool (0,1)
    df['swimming_pool'] = df['swimming_pool'].replace(-1,0)
    #Furnished (0,1)
    df['furnished'] = df['furnished'].replace(-1,0)
    #Open fire (0,1)
    df['open_fire'] = df['open_fire'].replace(-1,0)
    #Terrace (0,1)
    df['terrace'] = df['terrace'].replace(-1,0)
    #Terrace surface (float)
    df = df.loc[df['terrace_surface'] < 500]
    df['terrace_surface'] = df['terrace_surface'].replace(-1,0)
    #Facades (int)
    df = df.loc[df["number_of_facades"] < 9]
    df["number_of_facades"] = np.where((df["number_of_facades"] == -1) & (df["type_of_property"] == "APARTMENT"), 1, df["number_of_facades"])
    df["number_of_facades"] = np.where((df["number_of_facades"] == -1) & (df["type_of_property"] == "HOUSE"), 2, df["number_of_facades"])
    df = df.loc[df["number_of_facades"] != -1]
    #State of the building (int)
    df["state_of_the_building"] = df["state_of_the_building"].map({
        "NO_INFO": 0.87252, #"TO_RENOVATE"
        "TO_BE_DONE_UP": 0.65376, #"JUST_RENOVATED"
        "TO_RENOVATE": 0.56664, #"TO_RENOVATE"
        "TO_RESTORE": 0.46920, #"TO_REBUILD"
        "JUST_RENOVATED": 0.93115, #"JUST_RENOVATED"
        "GOOD": 0.79285, #"GOOD"
        "AS_NEW": 1.0 #"NEW"
    })
    #Type of property (category)¶
    df= df.loc[df["type_of_property"] != "OTHER"]
    ohe = OneHotEncoder()
    transformed_df = ohe.fit_transform(df[['type_of_property']])
    df[ohe.categories_[0]] = transformed_df.toarray()
    #price/m² calculate(float)
    df['price_m2'] = round(df['price']/df['surface'],2)
    #zipcode ratio calculate(float)
    df_zip_list = ['price_m2','zip_code_xx']
    df_zips = df[df_zip_list]
    xxx_zip = df_zips.groupby('zip_code_xx')
    xxx_zip_list = []  #stores the name of each zipcode from the data base
    for key, values in xxx_zip:
        xxx_zip_list.append(key)
    df_zips_mean = round(df_zips.groupby('zip_code_xx').mean(),5)
    df_zips_mean_values = df_zips_mean.values  # calculates mean for each zipxx
    zip_mean = [] # stores the values as a list of mean for each zipxx
    for x in df_zips_mean_values:
        for i in x:
            zip_mean.append(i)
    global_mean = statistics.median(zip_mean)  #calculate a global mean
    xxx = [] #list of the ponderated means 
    for y,i in enumerate(zip_mean):
        xxx.append(round(i/global_mean,2)) #calculates the relation of mean/zip code and the global mean
    dic_zip_value = dict()  #creates a dictionay for zipcodes and values
    for i,x in enumerate(xxx_zip_list):
        dic_zip_value[x] = xxx[i]
    df['zip_code_ratio'] = df['zip_code_xx']
    df['zip_code_ratio'] = df['zip_code_ratio'].map(dic_zip_value)

    #CLEAN DATA-------------------------------------------------------------

    filtered_atributes = [
                        'price',
                        #'id',
                        #'locality',
                        #'postal_code',
                        #'region',
                        #'province',
                        #'type_of_property',
                        #'subtype_of_property',
                        #'type_of_sale',
                        'number_of_bedrooms',
                        'surface',
                        #'kitchen_type',
                        'fully_equipped_kitchen',
                        #'furnished',
                        'open_fire',
                        #'terrace',
                        'terrace_surface',
                        'garden',
                        #'garden_surface',
                        #'land_surface',
                        'number_of_facades',
                        'swimming_pool',
                        'state_of_the_building',
                        #'zip_code_xx',
                        #'price_m2',
                        'zip_code_ratio',
                        'HOUSE',
                        'APARTMENT'
                        ]

    #filter the atributes that we need
    df = df[filtered_atributes]
    print('Data cleaned')

    #MODEL-------------------------------------------------------------------

    #split the data
    X = df.iloc[:,1:].values  #features
    Y = df.iloc[:,0].values  #target : price
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state=3)
    print('Data splited')

    #scale the data
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    #SAVE SCALER---------------------------------------------------------------
    with open("model/immo_scaler.pkl","wb") as scalefile:
        pickle.dump(scaler, scalefile)
        upload_file(local_file_path="model/immo_scaler.pkl", blob_name="immo_scaler_akl.pkl")
    print('Saved Scaler')


    #train the model
    poly_features = PolynomialFeatures(degree=3)
    # transforms the existing features to higher degree features.
    X_train_poly = poly_features.fit_transform(X_train)
    # fit the transformed features to Linear Regression
    poly_model = LinearRegression()
    poly_model.fit(X_train_poly, Y_train)

    #SAVE POLY FEATURES---------------------------------------------------------------
    with open("model/immo_poly_features.pkl","wb") as polyfeaturesfile:
        pickle.dump(poly_features, polyfeaturesfile)
        upload_file(local_file_path="model/immo_poly_features.pkl", blob_name="immo_poly_features_akl.pkl")
    print('Saved poly features')

    # predicting on training data-set
    y_train_predicted = poly_model.predict(X_train_poly)
    # predicting on test data-set
    y_test_predict = poly_model.predict(poly_features.fit_transform(X_test))

    # evaluating the model on training dataset
    rmse_train = np.sqrt(mean_squared_error(Y_train, y_train_predicted))
    r2_train = r2_score(Y_train, y_train_predicted)
    # evaluating the model on test dataset
    rmse_test = np.sqrt(mean_squared_error(Y_test, y_test_predict))
    r2_test = r2_score(Y_test, y_test_predict)

    #SAVE MODEL---------------------------------------------------------------
    with open("model/immo_model.pkl","wb") as modelfile:
        pickle.dump(poly_model, modelfile)
        upload_file(local_file_path="model/immo_model.pkl", blob_name="immo_model_akl.pkl")
    print('Saved Model')

    #RESULT------------------------------------------------------------------
    result = {'rmse_train':round(rmse_train,2),'r2_train':round(r2_train,2),'rmse_test':round(rmse_test,2),'r2_test':round(r2_test,2)}
    print(result)