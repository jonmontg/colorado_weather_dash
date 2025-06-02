from dash import html, dcc

def units_toggle():
  return html.Div([
    html.Label("Units:"),
    dcc.RadioItems(
      id="units-toggle",
      options=[
        {"label": "US", "value": "us"},
        {"label": "SI", "value": "si"}
      ],
      value="us",
      labelStyle={"display": "block"}
    ),
  ])