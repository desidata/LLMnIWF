import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pycountry

# Data
data = {
    "India": {"CEO": [50, 70], "Manager": [45, 60]},
    "USA": {"CEO": [50, 70], "Manager": [45, 60]},
    "UK": {"CEO": [45, 60], "Manager": [40, 50]},
    "Germany": {"CEO": [45, 60], "Manager": [40, 50]},
    "Japan": {"CEO": [50, 70], "Manager": [45, 60]},
    "China": {"CEO": [50, 70], "Manager": [48, 60]},
    "Brazil": {"CEO": [48, 65], "Manager": [44, 55]},
    "South Africa": {"CEO": [45, 60], "Manager": [40, 50]},
    "Australia": {"CEO": [45, 60], "Manager": [40, 50]},
    "Canada": {"CEO": [45, 60], "Manager": [40, 50]}
}

# Convert country names to ISO Alpha-3 codes
def get_country_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return country_name[:3].upper()  # Fallback if not found

# Convert data into a DataFrame
df = []
for country, values in data.items():
    for category, hours in values.items():
        df.append({
            'Country': get_country_code(country),
            'Category': category,
            'Min Hours': hours[0],
            'Max Hours': hours[1]
        })

df = pd.DataFrame(df)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Work Hours for CEOs and Managers Across the Globe", 
            style={'text-align': 'center', 'color': 'white'}),
    
    dcc.Graph(id='world-map', style={'height': '80vh'}),

    html.Div([
        html.Button("Play", id="play-button", n_clicks=0, style={'margin-right': '10px'}),
        html.Button("Pause", id="pause-button", n_clicks=0)
    ], style={'text-align': 'center', 'margin-top': '20px'})
])

@app.callback(
    Output('world-map', 'figure'),
    [Input('play-button', 'n_clicks'),
     Input('pause-button', 'n_clicks')]
)
def update_map(play_clicks, pause_clicks):
    fig = go.Figure()

    # Separate CEO and Manager data
    df_ceo = df[df['Category'] == "CEO"]
    df_manager = df[df['Category'] == "Manager"]

    # Offsets for overlapping countries
    offsets = {
        "USA": 0.5,
        "Canada": -0.5
    }

    # Animation frames
    frames = []
    for i in range(1, len(df_ceo) + 1):
        frames.append(go.Frame(
            data=[
                go.Scattergeo(
                    locations=df_ceo.iloc[:i]["Country"],
                    locationmode="ISO-3",
                    mode="markers+text",
                    text=df_ceo.iloc[:i]["Country"] + 
                         "<br><b>CEO:</b> " + df_ceo.iloc[:i]["Min Hours"].astype(str) + 
                         "-" + df_ceo.iloc[:i]["Max Hours"].astype(str) + " hrs",
                    marker=dict(
                        size=df_ceo.iloc[:i]["Max Hours"] / 2,
                        color="blue",
                        opacity=0.7,  # Slightly more opaque
                        line=dict(width=2, color="white")
                    ),
                    textposition="top center",
                    textfont=dict(size=16, color="white", family="Arial Black")
                ),
                go.Scattergeo(
                    locations=df_manager.iloc[:i]["Country"],
                    locationmode="ISO-3",
                    mode="markers+text",
                    text=df_manager.iloc[:i]["Country"] + 
                         "<br><b>Manager:</b> " + df_manager.iloc[:i]["Min Hours"].astype(str) + 
                         "-" + df_manager.iloc[:i]["Max Hours"].astype(str) + " hrs",
                    marker=dict(
                        size=df_manager.iloc[:i]["Max Hours"] / 2,
                        color="red",
                        opacity=0.7,
                        line=dict(width=2, color="white")
                    ),
                    textposition="bottom center",
                    textfont=dict(size=16, color="white", family="Arial Black")
                )
            ]
        ))

    # Initial empty traces
    fig.add_trace(go.Scattergeo(
        locations=[], locationmode="ISO-3", mode="markers+text", marker=dict(size=0)
    ))
    fig.add_trace(go.Scattergeo(
        locations=[], locationmode="ISO-3", mode="markers+text", marker=dict(size=0)
    ))

    # Update layout
    fig.update_layout(
        title="Work Hours for CEOs and Managers Across the World",
        geo=dict(
            showland=True,
            landcolor="brown",
            showcoastlines=True,
            coastlinecolor="white",
            showocean=True,
            oceancolor="#F8F8F8",  # Off-white ocean
            projection_type="natural earth"
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white"),
        margin=dict(r=0, t=50, l=0, b=0),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "x": 0.15,
            "y": -0.05,
            "xanchor": "right",
            "yanchor": "bottom",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 1000, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 500, "easing": "elastic-in-out"}
                    }]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [[None], {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate",
                        "transition": {"duration": 0}
                    }]
                }
            ]
        }]
    )

    # Apply animation frames
    fig.update(frames=frames)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
 










 