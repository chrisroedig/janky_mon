import requests
import time

LAT= '39.954714'
LNG= '-83.005839'
API_KEY='077ffff879ddbc16be03caa9d8e4b917'

GLOBAL_DATA = {
    'current': {},
    'last_update': None,
    }


def get_weather():
  if GLOBAL_DATA['last_update'] is None:
    update_weather()
  if time.time() - GLOBAL_DATA['last_update'] > 600:
    update_weather()
  return GLOBAL_DATA['current']

def update_weather():
    GLOBAL_DATA['current'] = request_weather()
    GLOBAL_DATA['last_update'] = time.time()

def request_weather():
  url = "https://api.darksky.net/forecast/{}/{},{}".format(API_KEY, LAT, LNG)
  resp = requests.get(url)
  if resp.status_code!= 200:
    return {}
  try:
    return resp.json()
  except:
    raise Exception(resp.text)
