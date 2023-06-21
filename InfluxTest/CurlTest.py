import requests

url = 'http://homedots.us:8086/write?db=shake'
payload = "cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000"

response = requests.post(url, data=payload)

print(response.status_code)
print(response.content)

    