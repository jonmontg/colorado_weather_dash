import requests
from pathlib import Path
import os
import json
from datetime import datetime, timedelta
from time import sleep

def _headers():
  return {
    "User-Agent": "COWeatherClient (jmontgom543@gmail.com.com)",
    "Accept": "application/geo+json; units=si"
  }

def was_file_created_within_last(filepath, hour=24):
    if not os.path.exists(filepath):
        return False
    creation_time = os.path.getctime(filepath)
    creation_dt = datetime.fromtimestamp(creation_time)
    one_hour_ago = datetime.now() - timedelta(hours=hour)
    return creation_dt > one_hour_ago

def _get_colorado_stations():
  cache_path = Path("cache", "stations.json")
  if os.path.exists(cache_path):
    with open(cache_path, "r") as f:
      return json.load(f)
    url = "https://api.weather.gov/stations"
    stations = []
    while url:
      resp = requests.get(url, headers=_headers(), params={"state": "CO"})
      if resp.status_code != 200:
        raise Exception(f"Failed to retrieve stations: {resp.text}")
      data = resp.json()
      if len(data["features"]) == 0:
         break
      for station in data["features"]:
        stations.append((
            station["id"],
            station["properties"]["name"],
            station["geometry"]["coordinates"]
        ))
      url = data.get("pagination", {}).get("next")
    with open(cache_path, "w") as f:
       json.dump(stations, f)
    return stations

def get_colorado_observations():
  stations = _get_colorado_stations()
  cache_path = Path("cache", "observations.json")
  if was_file_created_within_last(cache_path):
    with open(cache_path, "r") as f:
      return json.load(f)
  observations = []
  for sid, name, coords in stations:
    resp = requests.get(f"{sid}/observations/latest", headers=_headers())
    if resp.status_code != 200:
      print(f"Failed to retrieve station {sid} observation: {resp.text}")
      continue
    observations.append({
      name,
      coords,
      resp.json()["properties"]
    })
    sleep(0.5)
  with open(cache_path, "w") as f:
    json.dump(observations, f)
  return observations

def get_forecast(lat, lon):
  resp = requests.get(f"https://api.weather.gov/points/{lat},{lon}", headers=_headers())
  if resp.status_code != 200:
    return False, f"Failed to retrieve station forecast URL: {resp.status_code}"
  forecast_url = resp.json()["properties"]["forecastHourly"]
  resp = requests.get(forecast_url, headers=_headers())
  if resp.status_code != 200:
    return False, f"Failed to retrieve station forecast: {resp.status_code}"
  return True, resp.json()


