from dash import html, dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.data import get_forecast
from lib.units import *

def forecast(mark, units):
  lat = (mark["lat_lo"] + mark["lat_hi"]) / 2
  lon = (mark["lon_lo"] + mark["lon_hi"]) / 2
  success, value = get_forecast(lat, lon)

  if success:
    periods = value["properties"]["periods"][:24]
    temperature = [convert_temp(p["temperature"], "us", units) for p in periods]
    wind_speed = [convert_speed(float(p["windSpeed"].split()[0]), "us", units) for p in periods]
    precip_prob = [p["probabilityOfPrecipitation"]["value"] or 0 for p in periods]
    labels = [i+1 for i in range(24)]

    fig = make_subplots(
      rows=3, cols=1,
      shared_xaxes=True,
      vertical_spacing=0.1
    )

    fig.add_trace(go.Scatter(x=labels, y=temperature, name=f"Temp ({temp_units(units)})", mode="lines+markers"), row=1, col=1)
    fig.add_trace(go.Scatter(x=labels, y=wind_speed, name=f"Wind ({speed_units(units)})", mode="lines+markers"), row=2, col=1)
    fig.add_trace(go.Scatter(x=labels, y=precip_prob, name="Precip (%)", mode="lines+markers"), row=3, col=1)

    fig.update_yaxes(title_text=f"Temp ({temp_units(units)})", row=1, col=1)
    fig.update_yaxes(title_text=f"Wind ({speed_units(units)})", row=2, col=1)
    fig.update_yaxes(title_text="Precip (%)", row=3, col=1)
    fig.update_xaxes(title_text="Future (hours)", row=3, col=1)
    fig.update_layout(showlegend=False)
    fig.update_layout(
      margin=dict(l=0, r=0, t=0, b=0)
    )

    return html.Div([
      html.H3("24-Hour Forecast"),
      dcc.Graph(figure=fig)
    ])
  else:
    return html.Div(str(value), style={"color": "red", "padding": "10px"})