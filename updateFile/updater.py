import threading
import requests
import json

PATH="http://localhost:5000/"

def update_status():
  threading.Timer(6.0, update_status).start()
  allUrlsRes = requests.get(PATH + 'urls')
  allUrls = json.loads(allUrlsRes.text)
  print(allUrls)
  for url in allUrls:
      print(url)
      status = requests.get(url['url'])
      requests.put(PATH + 'url/' + str(url['id']), data={'status_code': status.status_code})





update_status()