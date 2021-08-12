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


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',options=[{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'KSC LC-39A ', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'All Sites', 'value': 'ALL'}],value='ALL',placeholder="Select a Launch Site",
                                                style={'textAlign': 'left', 'color': '#503D36',
                                               'font-size':'20px' ,'width':'80%','padding':'3px'},searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',min=0,
                                                max=10000,
                                                step=1000,
                                                value=[ min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value')]
)
def generate_chart(site_dropdown):
    dff=spacex_df
    if(site_dropdown=='ALL'):
        fig = px.pie(data_frame=dff, names='Launch Site',values='class')
        return (fig)
    else:
        data_div1=dff[["Launch Site","class"]]
        sec1=data_div1[data_div1['Launch Site']==site_dropdown]
        sec1=pd.DataFrame(sec1.value_counts())
        sec1.reset_index(inplace=True)
        sec1 = sec1.rename(columns={0:"outcome"})
        sec2=sec1[["class","outcome"]]
        fig = px.pie(data_frame=sec2, names='class',values='outcome')
        return (fig)
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
    Input(component_id="payload_slider", component_property="value")]
)
def scatter_chart(site_dropdown,payload_slider):
    dff=spacex_df
    if(site_dropdown=='ALL'):
        fig = px.scatter(dff, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return(fig)
    else:
        sec3=dff[["Launch Site","class","Payload Mass (kg)","Booster Version Category"]]
        sec4=sec3[sec3['Launch Site']==site_dropdown]
        fig = px.scatter(sec4, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return(fig)

# Run the app
if __name__ == '__main__':
    app.run_server()
