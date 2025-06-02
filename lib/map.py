from lib.data import get_colorado_observations
from math import cos, radians
import numpy as np
from collections import defaultdict

def valid_qual(feat):
    return feat["qualityControl"] == "V" or feat["qualityControl"] == "C"

def feat_median(xs, feat):
    values = [x[feat]["value"] for x in xs if valid_qual(x[feat])]
    return np.median(values) if values else np.nan

def temp_color(value, vmin=-10, vmax=30):
    if np.isnan(value):
        return "gray"
    ratio = min(max((value - vmin) / (vmax - vmin), 0), 1)
    r = int(255 * ratio)
    g = 0
    b = int(255 * (1 - ratio))
    return f'#{r:02x}{g:02x}{b:02x}'

def get_colorado_markers():
    obs = get_colorado_observations()

    min_lat, max_lat = 37.0, 41.0
    min_lon, max_lon = -109.05, -102.05
    lat_deg_per_5_miles = 5 / 69.0
    lon_deg_per_5_miles = 5 / (69.0 * cos(radians(39.0)))

    lat_points = np.arange(min_lat, max_lat+1, lat_deg_per_5_miles)
    lon_points = np.arange(min_lon, max_lon+1, lon_deg_per_5_miles)

    grid_buckets = defaultdict(list)
    for o in obs:
      lon, lat = o[1]
      row = int((lat - min_lat) // lat_deg_per_5_miles)
      col = int((lon - min_lon) // lon_deg_per_5_miles)
      grid_buckets[(row, col)].append(o)

    def get_coord(posn):
        return lat_points[posn[0]], lon_points[posn[1]]

    markers = []
    for posn, ls in grid_buckets.items():
      wind_dir = feat_median([o for _, _, o in ls], "windDirection")
      wind_speed = feat_median([o for _, _, o in ls], "windSpeed")
      temp = feat_median([o for _, _, o in ls], "temperature")
      lat_lo, lon_lo = get_coord(posn)
      lat_hi, lon_hi = get_coord((posn[0]+1, posn[1]+1))
      color = temp_color(temp)
      popup = f"Wind Speed: {'NA' if np.isnan(wind_speed) else round(wind_speed)} kph\nTemp: {'NA' if np.isnan(temp) else round(temp)} C"
      markers.append({
          "lat_lo": lat_lo,
          "lon_lo": lon_lo,
          "lat_hi": lat_hi,
          "lon_hi": lon_hi,
          "color": color,
          "popup": popup,
          "wind_dir": wind_dir,
          "wind_speed": wind_speed,
          "temp": temp,
          "props": [o for _, _, o in ls]
      })

    return markers
