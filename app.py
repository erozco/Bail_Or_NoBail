# Author = Erick Orozco
# Date 11-01-2023


from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px


# convert needed data into workable pandas datafram
perday_df = pd.read_csv('LA_County_PerDay_Crime.csv')


# Figure 2 - Static so just preload
fig2 = px.line(
    perday_df, 
    x="Date Reported", y=['Male','Female'])
fig2.update_layout(title_text='Reported Crimes by Victim Sex', title_x=0.5)
    #create red shape to visualize when no bail was an active policy
fig2.add_shape(
    type="rect",
    xref="x", yref="y",
    x0='2020-04-13', y0=0,
    x1='2020-07-01', y1=max(perday_df[['Male','Female']].max()),
    line=dict(width=0),
    fillcolor="#ff0000",
    opacity = 0.2,
    name = 'No Cash Bail Period',
    showlegend = True,
)

# initialize dashboard app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crime in Los Angeles County - Bail or No Bail"

# split dashboard into 3 components
app.layout = html.Div(children=[
    html.Div(
        html.H1("Crime in Los Angeles County - Bail or No Bail",style={"text-decoration": "underline",'textAlign': 'center','background-color':'lightsteelblue'}),
        className = 'row',
    ),
    html.Div([
        dcc.Graph(id="graph1"),
        dcc.Checklist(
            id="checklist",
            options=["Total Crime", "Violent Crime", "Simple Assault","Property Crime","Misc. Crime"],
            value=["Total Crime", "Violent Crime"],
            inline=True
        ),
    ],className = 'row'),
    html.Div([
        html.Div([
            dcc.Graph(id="graph2"),
            dcc.Checklist(
                id="checklist2",
                options=['Asian', 'Black', 'Latino', 'Indigenous', 'Pacific Islander', 'White', 'Unknown Descent', 'South Asian'],
                value=["Latino","White","Asian", "Black"],
                inline=True
            ),
        ],className='six columns'),
        html.Div([
            dcc.Graph(
                id="graph3",
                figure=fig2
                ),
        ],className='six columns')
    ],className = 'row'),
    
])

# First callback: Allow to see different tpyes of crime per day
@callback(
    Output("graph1", "figure"), 
    Input("checklist", "value"))

def update_line_chart(crime_type):
    fig = px.line(
        perday_df, 
        x="Date Reported", y=crime_type)
    fig.update_layout(title_text='Reported Crimes by Crime Type', title_x=0.5)
    fig.add_shape(
        type="rect",
        xref="x", yref="y",
        x0='2020-04-13', y0=0,
        x1='2020-07-01', y1=perday_df['Total Crime'].max(),
        line=dict(width=0,),
        fillcolor="#ff0000",
        opacity = 0.2,
        name = 'No Cash Bail Period',
        showlegend = True,
    )
    return fig

# Second callback: Allow to see different Victim Descents per day
@callback(
    Output('graph2', 'figure'),
    Input('checklist2', 'value'))

def update_line_chart_2(descent):
    fig = px.line(
        perday_df, 
        x="Date Reported", y=descent)
    fig.update_layout(title_text='Reported Crimes by Victim Descent', title_x=0.5)
    fig.add_shape(
        type="rect",
        xref="x", yref="y",
        x0='2020-04-13', y0=0,
        x1='2020-07-01', y1=max(perday_df[descent].max()),
        line=dict(width=0,),
        fillcolor="#ff0000",
        opacity = 0.2,
        name = 'No Cash Bail Period',
        showlegend = True,
    )
    return fig

if __name__ == '__main__':
    app.run(debug=False)

