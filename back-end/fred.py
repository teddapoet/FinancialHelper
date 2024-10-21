import requests
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

FRED_URL = "api.stlouisfed.org"

def main():
  logger = logging.getLogger(__name__)
  logging.basicConfig(
    filename="collect.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
  )

  API_KEY = os.environ.get('FRED_API_KEY')
  if (API_KEY is None):
    logger.error("No API key found")
    return 1

  endpoint = "/fred/series/observations"

  # query params
  file_type = "json"
  series_id = "GDP"
  realtime_start = "1776-07-04" # min
  realtime_end = "9999-12-31"   # max
  limit = "100000"

  # build query
  query = "https://" + FRED_URL + endpoint + "?" 
  query += f"file_type={file_type}&"
  query += f"series_id={series_id}&"
  query += f"realtime_start={realtime_start}&"
  query += f"realtime_end={realtime_end}&"
  query += f"limit={limit}&"
  query += f"api_key={API_KEY}"

  # request
  response = requests.get(query)
  if (response.status_code >= 400):
    logging.error(f"Request failed with status code {response.status_code} - {response.text}")
    return 1
  raw_json = response.json()

  # extract data
  data = raw_json.get('observations')
  if (data is None):
    logging.error("Data does not follow expected format - no 'observations' key")
    return 1
  data = pd.DataFrame.from_dict(data)
  data = data[data['value'] != "."]
  data['value'] = data['value'].astype(float)
  data['date'] = pd.to_datetime(data['date'])
  plt.plot(data['date'], data['value'])
  plt.show()

if __name__ == "__main__":
  main()
