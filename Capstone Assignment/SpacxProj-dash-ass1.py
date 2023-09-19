# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#site drop down  options
sdd=[]
sdd.append({'label': 'All Sites', 'value': 'ALL'})
#uniq sites
us=spacex_df["Launch Site"].unique()
#{'label': 'site1', 'value': 'site1'}
for item in us:
    sdd.append({'label': item, 'value': item})


# Create a dash application
app = dash.Dash(__name__)

min_value=1000
max_value=6500
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                dcc.Dropdown(id='site-dropdown',options=sdd,placeholder='Select a Launch Site here', searchable=True,value='ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                
                                dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10000, step=1000,
                                                    marks={0: '0',
                                                    10000: '10000'},
                                                    value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    filtered_df = spacex_df
    if entered_site == 'ALL':
        exp_rec= filtered_df.groupby('Launch Site')['Flight Number'].sum()
        labels = exp_rec.index
        sizes = exp_rec.values
        fig = px.pie(
                values=sizes,
                labels=labels, 
                title="% of launches by site"
            )
        return fig
    else:
        # return the outcomes piechart for a selected site
        print("showing pie for site -->"+entered_site)
        filtered_df_new = filtered_df[filtered_df['Launch Site'] == entered_site]
        exp_rec= filtered_df_new.groupby('class')['Flight Number'].sum()
        labels = exp_rec.index
        sizes = exp_rec.values
        fig = px.pie(
                values=sizes,
                labels=labels,
                title="% of success for site ["+entered_site+"]"
            )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
#implement what this call back would do here

def get_scatta(entered_site,slider_value):
    print("entered site is -->"+entered_site)
    #print("slider_value is -->"+slider_value)
    fig=''
    if entered_site == 'ALL':
        #do something
        fig = px.scatter(spacex_df, y="class", x="Payload Mass (kg)", color="Booster Version Category")
    else:
        #do something
        filtered_df_new = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_new, y="class", x="Payload Mass (kg)", color="Booster Version Category")

    return fig
                

# Run the app
if __name__ == '__main__':
    app.run_server()
