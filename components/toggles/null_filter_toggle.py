from dash import html
import dash_daq as daq

def null_filter_toggle():
  return daq.ToggleSwitch(id="toggle-na", label="Remove N/A", value=False)