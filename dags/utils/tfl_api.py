import requests
import logging

def fetch_tfl_arrivals(station_id='940GZZLUKSX', window_seconds=1800):
    try:
        response = requests.get(f'https://api.tfl.gov.uk/StopPoint/{station_id}/Arrivals', timeout=10)
        response.raise_for_status()
        return [arr for arr in response.json() if arr['timeToStation'] <= window_seconds]
    except Exception as e:
        logging.error(f"Failed to fetch TfL data: {e}")
        raise