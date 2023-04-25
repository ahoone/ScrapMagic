import requests # à installer avec 'pip install requests'
response = requests.get("https://httpbin.org/user-agent")
# print(response.json())

headers = {"user-agent": "toto"}
response = requests.get("https://httpbin.org/user-agent", headers=headers)
# print(response.json())

response = requests.get("https://httpbin.org/headers")
# print(response.json())

import yaml

with open("headers.yml") as f_headers:
    browser_headers = yaml.safe_load(f_headers)
# print(browser_headers["Firefox"])

response = requests.get("https://httpbin.org/headers", headers=browser_headers["Firefox"])
# print(response.json())

response = requests.get("https://free-proxy-list.net/")

import pandas as pd
proxy_list = pd.read_html(response.text)[0]
proxy_list["url"] = "http://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)
print(proxy_list.head())

https_proxies = proxy_list[proxy_list["Https"] == "yes"]
https_proxies.count()

url = "https://httpbin.org/ip"
good_proxies = set()
headers = browser_headers["Chrome"]
for proxy_url in https_proxies["url"]:
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=2)
        good_proxies.add(proxy_url)
        print(f"Proxy {proxy_url} OK, added to good_proxy list")
    except Exception:
        pass
    
    #if len(good_proxies) >= 3:
    #    break

print(good_proxies)

url = "https://www.cardmarket.com/en/Magic"
for browser, headers in browser_headers.items():
    print(f"\n\nUsing {browser} headers\n")
    for proxy_url in good_proxies:
        proxies = proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        #print(requests.get(url, headers=headers, proxies=proxies, timeout=2))
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=2)
            print(response.json())
        except Exception:
            print(f"Proxy {proxy_url} failed, trying another one")