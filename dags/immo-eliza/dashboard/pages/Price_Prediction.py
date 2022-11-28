import dash
from dash import dcc, html, ctx, Input, Output, callback, State
import pandas as pd
import pickle
import numpy as np

dash.register_page(__name__)

df = pd.read_csv("merged.csv")
df_cp = df[['locality', 'postal_code']]
df_cp = df_cp.drop_duplicates(subset='locality', keep='first')
df_cp = df_cp.drop_duplicates(subset='postal_code', keep='first')
cities_list = list(df_cp['locality'].values)
cities_list.sort()


layout = html.Div(
    [   
        html.H1("Price Prediction", style={'text-align': 'center'}),
        html.Br(),
        html.B('Property Type (required)'),
        dcc.Dropdown(['APARTMENT', 'HOUSE'],'APARTMENT', id='property_type'),
        html.B('City (required)'),
        html.Br(),
        dcc.Dropdown(cities_list, id="locality", placeholder="City"),
        html.B('Postal Code (required)'),
        html.Br(),
        dcc.Input(id="postal_code", type="number", debounce=True, placeholder="Postal Code", min=1000, max=9999, required=True),
        html.Br(),
        html.B('Living area (required)'),
        html.Br(),
        dcc.Input(id="area", type="number", placeholder="Living area (m²)", required=True),
        html.Br(),
        html.B('Number of Rooms'),
        html.Br(),
        dcc.Input(id="rooms", type="number", placeholder="Number of rooms", required=True),
        html.Br(),
        html.B('Land area'),
        html.Br(),
        dcc.Input(id="land_area", type="number", placeholder="Land area (m²)"),
        html.Br(),
        dcc.Checklist(id='garden',options=['Garden'], value=[]),
        html.B('Garden area'),
        html.Br(),
        dcc.Input(id="garden_area", type="number", placeholder="Garden area (m²)"),
        dcc.Checklist(id='terrace',options=['Terrace'], value=[]),
        html.B('Terrace area'),
        html.Br(),
        dcc.Input(id="terrace_area", type="number", placeholder="Terrace area (m²)"),
        html.Br(),
        html.B('Number of Facades'),
        html.Br(),
        dcc.Input(id="facades", type="number", placeholder="Number of facades"),
        dcc.Checklist(id='kitchen',options=['Equipped kitchen'],value=[]),
        dcc.Checklist(id='pool',options=['Swimming Pool'],value=[]),
        dcc.Checklist(id='fire',options=['Open Fire'],value=[]),
        html.B('Building State'),
        dcc.Dropdown(['NEW', 'GOOD', 'TO RENOVATE', 'TO REBUILD', 'JUST RENOVATED'], id='property_state', placeholder='Select a building state'),
        html.Button('Predict Price', id='predict_button'),
        html.Button('Reset',id='reset_button'),
        html.Div(id='prediction', style={'whiteSpace': 'pre-line', 'font-size': '30px'})

    ],style={'display': 'inline-block',"margin-left": "15px"}
)


@callback(
    Output('postal_code', 'value'),
    Output('locality', 'value'),
    Output('area', 'value'),
    Output('rooms', 'value'),
    Output('land_area', 'value'),
    Output('garden_area', 'value'),
    Output('terrace_area', 'value'),
    Output('facades', 'value'),
    Output('property_state', 'value'),
    Output('garden', 'value'),
    Output('terrace', 'value'),
    Output('kitchen', 'value'),
    Output('pool', 'value'),
    Output('fire', 'value'),
    Output('reset_button','n_clicks'),
    Input('postal_code', 'value'),
    Input('locality', 'value'),
    Input('reset_button','n_clicks')
    )
def sync_input(postal_code, locality, n_clicks_reset):

    if n_clicks_reset is None:

        if ctx.triggered_id == 'locality':
            postal_code = None if locality is None else (df_cp.loc[df_cp['locality']==locality, 'postal_code']).to_string(index=False)
        else:
            locality = None if postal_code is None else (df_cp.loc[df_cp['postal_code']==postal_code, 'locality']).to_string(index=False)
        return postal_code, locality, dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update, None
    
    else:
        n_clicks_reset=None
        return '','','','','','','','',None,[],[],[],[],[], None


def get_zip_ratio(zip_code):
    #DICTIONARY OF ZIP CODE VALUES 
    zip_code_dict_xx = {
    'be_zip_10': 1.53,
    'be_zip_11': 1.68,
    'be_zip_12': 1.66,
    'be_zip_13': 1.29,
    'be_zip_14': 1.18,
    'be_zip_15': 1.24,
    'be_zip_16': 1.31,
    'be_zip_17': 1.23,
    'be_zip_18': 1.22,
    'be_zip_19': 1.5,
    'be_zip_20': 1.53,
    'be_zip_21': 1.17,
    'be_zip_22': 1.13,
    'be_zip_23': 1.12,
    'be_zip_24': 1.03,
    'be_zip_25': 1.24,
    'be_zip_26': 1.27,
    'be_zip_27': 1.11, 
    'be_zip_28': 1.22,
    'be_zip_29': 1.3,
    'be_zip_30': 1.58,
    'be_zip_31': 1.18,
    'be_zip_32': 1.1,
    'be_zip_33': 1.07,
    'be_zip_34': 0.87,
    'be_zip_35': 1.13,
    'be_zip_36': 1.0,
    'be_zip_37': 0.9,
    'be_zip_38': 0.94,
    'be_zip_39': 1.0,
    'be_zip_40': 0.93,
    'be_zip_41': 0.85,
    'be_zip_42': 0.86,
    'be_zip_43': 0.87,
    'be_zip_44': 0.81,
    'be_zip_45': 0.76,
    'be_zip_46': 0.95,
    'be_zip_47': 0.98,
    'be_zip_48': 0.85,
    'be_zip_49': 0.94,
    'be_zip_50': 0.97,
    'be_zip_51': 1.0,
    'be_zip_52': 0.77,  
    'be_zip_53': 0.87,
    'be_zip_54': 0.77,
    'be_zip_55': 0.76,
    'be_zip_56': 0.67,
    'be_zip_57': 0.77,
    'be_zip_58': 0.77,
    'be_zip_59': 0.77,
    'be_zip_60': 0.64,
    'be_zip_61': 0.74,
    'be_zip_62': 0.78,
    'be_zip_63': 0.69,
    'be_zip_64': 0.66,
    'be_zip_65': 0.67,
    'be_zip_66': 0.91,
    'be_zip_67': 0.97,
    'be_zip_68': 0.84,
    'be_zip_69': 0.83,
    'be_zip_70': 0.8,
    'be_zip_71': 0.69,
    'be_zip_72': 0.67,
    'be_zip_73': 0.58,
    'be_zip_75': 0.86,
    'be_zip_76': 0.66,
    'be_zip_77': 0.79,
    'be_zip_78': 0.91,
    'be_zip_79': 0.66,
    'be_zip_80': 1.34,
    'be_zip_81': 1.25,
    'be_zip_82': 1.32,
    'be_zip_83': 2.12,
    'be_zip_84': 1.43,
    'be_zip_85': 1.06,
    'be_zip_86': 1.61,
    'be_zip_87': 1.16,
    'be_zip_88': 0.98,
    'be_zip_89': 0.95,
    'be_zip_90': 1.46,
    'be_zip_91': 1.13,
    'be_zip_92': 1.11,
    'be_zip_93': 1.03,
    'be_zip_94': 1.0,
    'be_zip_95': 0.96,
    'be_zip_96': 0.94,
    'be_zip_97': 1.11,
    'be_zip_98': 1.27,
    'be_zip_99': 1.16
    }

    return zip_code_dict_xx['be_zip_'+str(zip_code)[:2]]


@callback(
    Output('prediction','children'),
    Output('predict_button','n_clicks'),
    Input('property_type', 'value'),
    Input('postal_code', 'value'),
    Input('area', 'value'),
    Input('rooms', 'value'),
    Input('terrace_area', 'value'),
    Input('facades', 'value'),
    Input('property_state', 'value'),
    Input('garden', 'value'),
    Input('kitchen', 'value'),
    Input('pool', 'value'),
    Input('fire', 'value'),
    Input('predict_button','n_clicks')
    )

def predict_price(property_type,postal_code,area,rooms,terrace_area,facades,property_state,garden,kitchen,pool,fire,n_clicks_predict):

    if n_clicks_predict is None:
        raise dash.exceptions.PreventUpdate

    else:

        n_clicks_predict=None

        property_values = []

        if rooms:
            property_values.append(rooms)
        else:
            property_values.append(0)
        
        if area < 10:
            property_values.append(10)
        else:
            property_values.append(area)

        if kitchen == []:
            property_values.append(0)
        else:
            property_values.append(1)

        if fire == []:
            property_values.append(0)
        else:
            property_values.append(1)
        
        if terrace_area:
            property_values.append(terrace_area)
        else:
            property_values.append(0)

        if garden == []:
            property_values.append(0)
        else:
            property_values.append(1)
        
        if facades:
            property_values.append(facades)
        else:
            property_values.append(2)

        if pool == []:
            property_values.append(0)
        else:
            property_values.append(1)
        
        prop_state_dict = {
        "NEW": 1.0,
        "JUST RENOVATED": 0.75,
        "GOOD": 0.5, #"GOOD"
        "TO RENOVATE": 0.25,
        "TO REBUILD": 0.25,
        None: 0.87252
        }

        property_values.append(prop_state_dict[property_state])

        zip_code_ratio = get_zip_ratio(postal_code)
        property_values.append(zip_code_ratio)

        if property_type == 'HOUSE':
            property_values.extend([1,0])
        else:
            property_values.extend([0,1])


        with open("model/immo_scaler.pkl", "rb") as scaler_file:
            scaler = pickle.load(scaler_file)
        
        with open("model/immo_poly_features.pkl", "rb") as poly_features_file:
            poly_features = pickle.load(poly_features_file)
        
        with open("model/immo_model.pkl", "rb") as model_file:
            model = pickle.load(model_file)
        
        array_input = np.array([property_values])
        X_scaled_input = scaler.transform(array_input)
        price_prediction = model.predict(poly_features.fit_transform(X_scaled_input))

        return f'Price prediction: {round(float(price_prediction), 2)} €', None



