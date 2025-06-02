from dash import html, dcc
import dash_leaflet as dl
from components.radio_buttons.map_marker_toggle import map_marker_toggle
from components.radio_buttons.units_toggle import units_toggle
from components.toggles.null_filter_toggle import null_filter_toggle

def layout():
  return html.Div([
    html.Div([
      html.H1("Colorado weather forecast"),
      html.Div([
        # Map
        dl.Map(
          center=[39, -105.5],
          zoom=7,
          style={'width': '1000px', 'height': '660px'},
          id="map"
        ),
        dcc.Store(id="selected-marker-index"),

        # Right-side panel
        html.Div([
          # Radio Buttons
          html.Div([
            map_marker_toggle(),
            null_filter_toggle(),
            units_toggle()
          ], style={"display": "flex", "gap": "30px"}),

          # Current weather
          html.Div(id="marker-output"),

          # Forecast Box
          html.Div(id="forecast-box")
        ], style={"marginLeft": "20px", "padding": "10px"})
      ], style={"display": "flex", "alignItems": "flex-start"})
    ])
  ])