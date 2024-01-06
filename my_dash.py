from datetime import date

from dash import Dash, dcc, html, Input
import plotly.express as px
from dash.dcc import DatePickerSingle
from dash.dependencies import Output
from get_data import FCApiService
from get_data import RestCountriesService
from get_data import MockAPIService
import pandas as pd

# Création de l'application Dash
app = Dash(__name__)

# Création des instances des services
service = RestCountriesService()
# API avec peu de requête :
current_service = service2 = FCApiService()
# Ajout d'une mockAPI pour qu'elle prenne le relai quand FCApiService n'a plus de requête
mockService = MockAPIService()

# Chargement des données pour la visualisation
df = px.data.tips()
fig = px.histogram(df, x="total_bill")
df = px.data.gapminder().query("year==2007")
data = service.get_countries()

# Création de la carte choropleth

fig2 = px.choropleth(
    data_frame=data,
    locations='cca3',
    projection='natural earth',
    labels={'currencies': 'Currency Code', 'countries': 'Country Name'},
    hover_data={'currencies': True, 'name': True},
    color='currencies',
)

# Définition des couleurs pour le style
colors = {
    'background': '#0b0c2a',
    'color': '#ffffff'
}

# Définition de la mise en page de l'application
app.layout = html.Div(style={'backgroundColor': colors['background'], 'width': '100%', 'margin': 0}, children=[
    # Section de l'en-tête
    html.Br(),
    html.H1(
        children='TAUX DE CHANGE ET DEVISE',
        style={
            'textAlign': 'center',
            'color': colors['color'],
            'font-family': 'Roboto',
            'margin': '20px auto'
        }
    ),
    # Section du convertisseur
    html.H2(
        children='Convertisseur :',
        style={
            'color': '#E9511A',
            'font-family': 'Roboto',
            'margin-left': '20px'

        }
    ),
    html.Div(
        children=[
            html.H3(
                children=f'Service Utilisé: {current_service.__class__.__name__}',
                style={
                    'color': colors['color'],
                    'font-family': 'Roboto',
                    'margin-left': '20px'
                }
            )
        ],
        style={'textAlign': 'left', 'margin-left': '20px'}
    ),
    # Listes déroulantes pour la sélection des devises
    html.Div(
        children=[
            dcc.Dropdown(
                options=[{"label": currency, "value": currency} for currency in service.get_currencies()],
                value='EUR',
                multi=False,
                placeholder="Select a first device",
                style={'width': '60%', 'margin': '10px auto'},
                id='dropdown1'  # Updated identifier
            ),
            dcc.Dropdown(
                options=[{"label": currency, "value": currency} for currency in service.get_currencies()],
                value='USD',
                multi=False,
                placeholder="Select a second device",
                style={'width': '60%', 'margin': '10px auto'},
                id='dropdown2'  # Updated identifier
            )

        ],
        style={'display': 'flex', 'justifyContent': 'center', 'textAlign': 'center', 'font-family': 'Roboto',
               'margin': '10px auto'}
    ),

    # Conteneur de sortie pour le résultat de la conversion
    html.Div(
        id='output-container-button',
        children=[
            html.Div([
                dcc.Input(id='input-box', type='text',
                          style={'textAlign': 'center', 'font-family': 'Roboto', 'margin': '10px auto',
                                 'width': '10%', 'height': '20%'}),
                html.Div(id='outputResult',
                         style={'color': colors['color'], 'font-family': 'Roboto', 'width': '10%',
                                'margin': '10px auto'})
            ], style={'textAlign': 'center', 'display': 'flex', 'flexDirection': 'row'}),
        ],
        style={'display': 'block', 'justifyContent': 'center', 'align-item': 'center'}
    ),
    html.Br(),
    # Titre de l'histogramme
    html.H2(
        children=' Histogramme :',
        style={
            'color': '#EF855E',
            'font-family': 'Roboto',
            'margin-left': '20px'

        }
    ),
    html.Div(
        id='input-container-button-histogramme',
        children=[

            html.Div([
                dcc.Dropdown(
                    options=[{"label": year, "value": year} for year in list(range(2000, 2023 + 1))],
                    value='2023',
                    multi=False,
                    placeholder="Select a year",
                    style={'width': '60%', 'margin': '10px auto'},
                    id='input-box-year'  # Updated identifier
                ),
                dcc.Dropdown(
                    options=[{"label": week, "value": week} for week in list(range(1, 51 + 1))],
                    value='1',
                    multi=False,
                    placeholder="Select a week",
                    style={'width': '60%', 'margin': '10px auto'},
                    id='input-box-week'  # Updated identifier
                )
            ],
                style={'display': 'flex', 'justifyContent': 'center', 'textAlign': 'center', 'font-family': 'Roboto',
                       'margin': '10px auto'}
            ),
            # Section de l'histogramme
            dcc.Graph(
                id='histogramme',
                figure=fig
            ),
            html.Br(),

            # Titre de la map
            html.H2(
                children='Map :',
                style={
                    'color': colors['color'],
                    'font-family': 'Roboto',
                    'margin-left': '20px'

                }
            ),
            # Section de la map
            dcc.Graph(
                id='map',
                figure=fig2,
                style={'height': 700}
            ),

        ])])

# Design de l'histogramme
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['color'],
)
# Design de la map
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['color'],
)


# Callback function pour gérer la soumission ou la perte de focus
@app.callback(
    Output(component_id='outputResult', component_property='children'),
    [Input(component_id='dropdown1', component_property='value'),
     Input(component_id='dropdown2', component_property='value'),
     Input(component_id='input-box', component_property='value')],
)
def handle_submit_or_blur(from_currency, to_currency, amount):
    if from_currency and to_currency and amount:
        # Appel de la fonction convert_currency du service mockService
        global current_service
        try:
            current_service = service2
            return service2.convert_currency(from_currency, to_currency, float(amount))
        except :
            current_service = mockService
            return mockService.convert_currency(from_currency, to_currency, float(amount))

# Callback function pour mettre à jour l'histogramme
@app.callback(
    Output('histogramme', 'figure'),
    [Input(component_id='dropdown1', component_property='value'),
     Input(component_id='dropdown2', component_property='value'),
     Input(component_id='input-box-year', component_property='value'),
     Input(component_id='input-box-week', component_property='value'),
     ]
)
def update_histogramme(from_symbol, to_symbol, year, week):
    if from_symbol and to_symbol and year and week:
        try :
            exchange_rates = service2.get_exchange_rate_history(from_symbol, to_symbol, int(year), int(week))
        except:
            exchange_rates = mockService.get_exchange_rate_history(from_symbol, to_symbol, int(year), int(week))

        # Créer un DataFrame à partir des taux de change
        df = pd.DataFrame({'Date': list(exchange_rates.keys()), 'Exchange Rate': list(exchange_rates.values())})
        fig = px.bar(df, x="Date", y="Exchange Rate", barmode="group")
        fig.update_traces(marker_color="#EF855E")
        fig.update_layout(
            plot_bgcolor="#0b0c2a",
            paper_bgcolor="#0b0c2a",
            font_color="white"
        )
        return fig


def reset_map(fig):
    fig.update_geos(clickmode='event+reset')
