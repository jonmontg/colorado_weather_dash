from dash import Dash, Output, Input, ALL
import dash
import json
import dash_leaflet as dl
import numpy as np
from lib.map import get_colorado_markers
from components.weather_table import weather_table
from components.forecast import forecast
from components.map_markers.temperature import temperature_marker
from components.map_markers.wind import wind_marker
from components.layout import layout

app = Dash(__name__)

# Load markers
marker_data = get_colorado_markers()

app.layout = layout()

# Radio Button callback. Changes the map-marker display
@app.callback(
  Output("map", "children"),
  [
    Input("data-toggle", "value"),
    Input("toggle-na", "value")
  ],
)
def toggle_map_data(data, remove_na):
  markers = []
  if data == "temp":
    markers = [temperature_marker(m, i) for i, m in enumerate(marker_data) if not remove_na or not np.isnan(m["temp"])]
  elif data == "wind":
    markers = [wind_marker(m, i) for i, m in enumerate(marker_data) if not remove_na or not np.isnan(m["wind_speed"])]
  return [
    dl.TileLayer(),
    dl.LayerGroup(markers, id=f"layer-{data}")
  ]

# Set the selected-marker-index data store
@app.callback(
  Output("selected-marker-index", "data"),
  Input({"type": "marker-click", "index": ALL, "marker_index": ALL}, "n_clicks"),
  prevent_initial_call=True
)
def set_selected_marker(n_clicks):
  ctx = dash.callback_context
  if not ctx.triggered or not any(n_clicks):
    return dash.no_update
  triggered_id = json.loads(ctx.triggered[0]["prop_id"][:-9])
  return triggered_id["marker_index"]

# Map Marker selection callback. Adds a div below the map to show regional details
@app.callback(
  Output("marker-output", "children"),
  [
    Input("selected-marker-index", "data"),
    Input("units-toggle", "value"),
    Input("data-toggle", "value")
  ],
  prevent_initial_call=True
)
def display_details(midx, units, _):
  if midx is None:
    return dash.no_update
  mark = marker_data[midx]
  return weather_table({"temp": mark["temp"], "wind_speed": mark["wind_speed"], "wind_dir": mark["wind_dir"]}, units)

# Map Marker selection callback. Adds a div to the right of the map to display forecast plots
@app.callback(
  Output("forecast-box", "children"),
  [
    Input("selected-marker-index", "data"),
    Input("units-toggle", "value"),
    Input("data-toggle", "value")
  ],
  prevent_initial_call=True
)
def display_forecast(midx, units, _):
  if midx is None:
    return dash.no_update
  mark = marker_data[midx]
  return forecast(mark, units)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8055)
