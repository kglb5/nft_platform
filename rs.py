import requests
url = "https://api.ipify.org?format=json"

r = requests.get(url)
print(r.text)
# import requests as r
# from requests.auth import HTTPProxyAuth
#
# proxy = {
#               "http"  : "http://raj:password@45.77.86.71:8080",
#               "https" : "https://user:password@45.77.86.71:8080",
#             }
#
# auth = HTTPProxyAuth("raj", "rj450S@")
#
# response = r.get("http://youtube.com", proxies=proxy, auth=auth)
#
# print(response.text)
