from dash import html, dcc

def map_marker_toggle():
  return html.Div([
    html.Label("Select map type:"),
    dcc.RadioItems(
      id="data-toggle",
      options=[
        {"label": "Temperature", "value": "temp"},
        {"label": "Wind Speed", "value": "wind"}
      ],
      value="temp",
      labelStyle={"display": "block"}
    ),
  ])