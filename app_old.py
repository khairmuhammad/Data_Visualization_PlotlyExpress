import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
server = app.server



styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#Read dataset
df = pd.read_csv("gapminder.csv")
dff = df.copy()
#List of dataset columns
available_indicators = list(df)

#list of countries
country_test = list(df.country)
countries = [] 
[countries.append(x) for x in country_test if x not in countries]

#list of years
years = list(df.year)


app.layout = html.Div([
	html.H1("Dashboard for My Visualization Work done in Plotly Express", style={'textAlign': 'center', 'color': 'Black'}),
	html.H2("Scatter Plot", style={'textAlign': 'center', 'color': 'Blue'}),
	html.P("This scatter plot shows the continent-wise growth of life expectancy and GDP per Capita of countries. Along with that it also shows population, country name, continent and life expectancy on hovering.",
	style={'textAlign': 'center'}),
    dcc.Graph(id='graph-with-slider'),
	html.P("Slide the years below to see the scatter plot for that year",
	style={'textAlign': 'center'}),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
	html.Br(),
	html.H2("Bar Chart", style={'textAlign': 'center', 'color': 'Red'}),
	html.P("This bar chart shows the yearly life expectancy of the selected country. Along with that it also shows population and gdp per capita on hovering.",
	style={'textAlign': 'center'}),
	dcc.Graph(id='graph-with-dropdown'),
    html.P("Select country for which you want to show Bar Plot",
	style={'textAlign': 'center'}),
	dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in countries],
        value=countries[0]
    )
])




#Callback for Scatter Plot
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdp_cap", y="life_exp", 
                     size="population", color="continent", hover_name="country", 
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
	
	

#Callback for Bar Plot
@app.callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('country-dropdown', 'value')])
def update_figure(selected_country):
    filtered_df = df[df.country == selected_country]

    fig = px.bar(filtered_df, x='year', y='population',
             hover_data=['life_exp', 'gdp_cap'], color='life_exp',
             labels={'population':'population of Canada'}, height=400)

    fig.update_layout(transition_duration=500)

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)