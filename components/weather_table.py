from dash import html
import numpy as np
from lib.units import *

def angle_to_direction(angle):
  if np.isnan(angle):
    return "N/A"
  directions = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
  ]
  index = int(((angle + 11.25) % 360) / 22.5)
  return directions[index]

def fmt(x, label):
  if np.isnan(x):
    return "N/A"
  return f"{str(round(x, 2))} {label}"

def weather_table(data, units):
  temp = convert_temp(data["temp"], "si", units)
  speed = convert_speed(data["wind_speed"], "si", units)
  return html.Div([
    html.H3("Current Weather"),
    html.Table([
      html.Tbody([
        html.Tr([html.Td("Temperature:"), html.Td(fmt(temp, temp_units(units)))]),
        html.Tr([html.Td("Wind Speed:"), html.Td(fmt(speed, speed_units(units)))]),
        html.Tr([html.Td("Wind Direction:"), html.Td(angle_to_direction(data["wind_dir"]))])
      ])
    ], id="weather-table", style={"border": "none", "height": "40px", "width": "400px"})
  ])