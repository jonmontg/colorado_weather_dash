import numpy as np
import dash_leaflet as dl

def wind_marker(marker, i):
  opacity = 0.1
  if np.isnan(marker["wind_speed"]):
    opacity = 0.5
  else:
    opacity += min(1, (marker["wind_speed"] / 50)) * 0.9

  return dl.Rectangle(
    id={
        "type": "marker-click",
        "index": f"{marker['lat_lo']:.4f}_{marker['lon_lo']:.4f}",
        "marker_index": i
      },
      bounds = [
        [marker["lat_lo"], marker["lon_lo"]],
        [marker["lat_hi"], marker["lon_hi"]]
      ],
      fill=True,
      fillOpacity=opacity,
      opacity=opacity,
      color="grey" if np.isnan(marker["wind_speed"]) else "blue"
    )