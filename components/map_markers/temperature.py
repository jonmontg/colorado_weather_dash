import dash_leaflet as dl

def temperature_marker(marker, i):
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
      fillOpacity=0.4,
      color=marker["color"]
    )