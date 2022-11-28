import pandas as pd
import dash
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from utils.download_file import download_file

#download_file("model/immo_model.pkl", "immo_model_akl.pkl")
#download_file("model/immo_scaler.pkl", "immo_scaler_akl.pkl")
#download_file("model/immo_poly_features.pkl", "immo_poly_features_akl.pkl")

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

app.layout = html.Div(
    [
        # main app framework
        html.Div("Immo Eliza", style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'], style={"margin-left": "15px"})
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True,port=8050)
