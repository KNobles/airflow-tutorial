import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, State
import dash
from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go




dash.register_page(__name__, path='/')

df = pd.read_csv("properties.csv")
df = df[df['price']>=0]
df_cp = pd.read_csv("belgian-cities-geocoded.csv")
df_cp = df_cp[['postal', 'lat', 'lng']]
df_cp.rename(columns={'postal':'postal_code'}, inplace=True)
df = df.merge(df_cp, on='postal_code')
df_merged = df.drop('Unnamed: 0', axis=1)
# df.to_csv('merged.csv', index=False)
df_corr = df[['price', 'province', 'type_of_property', 'number_of_bedrooms', 'surface', 'fully_equipped_kitchen', 'furnished', 'open_fire', 'terrace', 
'terrace_surface','garden', 'garden_surface', 'land_surface', 'number_of_facades', 'swimming_pool', 'state_of_the_building']]

cat_values = ['region', 'province', 'type_of_property', 'subtype_of_property', 'fully_equipped_kitchen', 'furnished', 'open_fire', 'terrace', 'garden', 'swimming_pool', 'state_of_the_building']
cont_values = ['number_of_bedrooms', 'surface', 'terrace_surface', 'garden_surface', 'land_surface', 'number_of_facades']

df_map = df.groupby(['region'])[['price', 'lat', 'lng']].mean()
df_map = df_map.reset_index()

fig = px.scatter_mapbox(
    data_frame=df_map,
    lat='lat',
    lon='lng',
    color='price',
    size='price',
    hover_data=['region', 'price'],
    color_continuous_scale=px.colors.sequential.thermal,
    size_max=40,
    template='plotly_dark',
    mapbox_style='stamen-terrain',

)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, clickmode= 'event+select')


# App layout
layout = html.Div([
    html.H1("Dashboard", style={'text-align': 'center'}),
    html.H2("Interactive map", style={'text-align': 'left'}),
    dcc.Graph(id='mean price map', figure=fig,style={'height': '80vh'}),
    html.Button('Reset map', id='reset_map'),
    html.Br(),
    html.H2("Correlations", style={'text-align': 'left'}),
    dcc.Dropdown(id='features' ,multi=True, value=df_corr.columns, options=[{'label': x, 'value': x} for x in df_corr.columns]),
    dcc.Graph(id='correlations', figure={},style={'height': '80vh'}),
    html.Br(),
    dcc.Dropdown(id='cities' ,multi=True, value=[], options=[{'label': x, 'value': x} for x in df['locality'].unique()]),
    dcc.Dropdown(id='type', multi=True,value=[],options=[{'label': x, 'value': x} for x in df['type_of_property'].unique()]),
    dcc.Graph(id='bars', figure={},style={'height': '80vh'})
])


@callback(
    Output(component_id='mean price map', component_property='figure'),
    Output('reset_map','n_clicks'),
    Input(component_id='mean price map', component_property='clickData'),
    Input('reset_map','n_clicks'),
    State('mean price map', 'figure'))
def show_map(click_data, n_clicks, figure):
    # print('initial reset button ', n_clicks)
    # print('click click: ',click_data)
    if click_data:

        if n_clicks:
            # print('after ',n_clicks)
            fig = px.scatter_mapbox(
                data_frame=df_map,
                lat='lat',
                lon='lng',
                color='price',
                size='price',
                hover_data=['region', 'price'],
                color_continuous_scale=px.colors.sequential.thermal,
                size_max=40,
                template='plotly_dark',
                mapbox_style='stamen-terrain',

            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, clickmode= 'event+select')
            return fig, None

        choice = click_data['points'][0]['customdata'][0]
        click_data = None
        # print('choice: ', choice)

        if choice in list(df['region'].unique()):
            # print(f'click data: {choice}')
            # print('region chosen')
            df_region = df[df['region']==choice]
            df_province = df_region.groupby(['province'])[['price', 'lat', 'lng']].mean()
            df_province = df_province.reset_index()
            figure = px.scatter_mapbox(
                data_frame=df_province,
                lat='lat',
                lon='lng',
                color='price',
                size='price',
                hover_data=['province', 'price'],
                color_continuous_scale=px.colors.sequential.thermal,
                size_max=40,
                template='plotly_dark',
                mapbox_style='open-street-map',
            )
            figure = figure.update_layout(overwrite=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, clickmode= 'event+select')

            return figure, None

        if choice in list(df['province'].unique()):
            # print('province chosen')
            # print(f'click data: {choice}')
            df_province = df[df['province']==choice]
            df_locality = df_province.groupby(['locality'])[['price', 'lat', 'lng']].mean()
            df_locality = df_locality.reset_index()
            figure = px.scatter_mapbox(
                data_frame=df_locality,
                lat='lat',
                lon='lng',
                color='price',
                size='price',
                hover_data=['locality', 'price'],
                color_continuous_scale=px.colors.sequential.thermal,
                size_max=40,
                template='plotly_dark',
                mapbox_style='carto-positron',
            )
            figure = figure.update_layout(overwrite=True, margin={"r": 0, "t": 0, "l": 0, "b": 0}, clickmode= 'event+select')

            return figure, None
        

    return dash.no_update

@callback(
    Output(component_id='correlations', component_property='figure'),
    Input(component_id='features', component_property='value'))
def update_corr(corr_pick):
    df_correlations = df_corr[corr_pick].corr()
    x = list(df_correlations.columns)
    y = list(df_correlations.index)
    z = df_correlations.values

    fig_corr = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=np.around(z, decimals=2),
        hoverinfo='z',
        colorscale='Blues'
    )
    return fig_corr


@callback(
    Output(component_id='bars', component_property='figure'),
    Input(component_id='cities', component_property='value'),
    Input(component_id='type',component_property='value'))
def show_bars(cities, property_type):

    df = df_merged[['locality','type_of_property','price']]
    df = df.groupby(['locality','type_of_property'],as_index=False)['price'].mean()


    if property_type==[] and cities==[]:
        fig_bar=px.bar()
    else:
        if property_type==[]:
            df_bars = df[df['locality'].isin(cities)]
        elif cities==[]:
            df_bars = df[df['type_of_property'].isin(property_type)]
        else:
            df_bars = df[df['locality'].isin(cities) & df['type_of_property'].isin(property_type)]
        
        fig_bar = px.bar(
            data_frame=df_bars,
            x='locality',
            y='price',
            color= 'type_of_property',
            barmode='group',
            labels={'x':'Cities', 'y':'Mean Price'}
        )

    return fig_bar