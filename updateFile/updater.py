import threading
import requests
import json

PATH="http://172.17.0.1:5000/"

def update_status():
  threading.Timer(6.0, update_status).start()
  allUrlsRes = requests.get(PATH + 'urls')
  allUrls = json.loads(allUrlsRes.text)
  print(allUrls)
  for url in allUrls:
      t = threading.Thread(target=run_urls, args=[url])
      t.start()


def run_urls(url):
    print(url)
    status = requests.get(url['url'])
    requests.put(PATH + 'urls', json={'id': str(url['id']), 'status_code': status.status_code})





update_status()