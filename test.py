import requests

url = "https://api.avalai.ir/user/credit"
headers = {
 "Content-Type": "application/json",
 "Authorization": "Bearer aa-ECEziRAGW0ItBr2IqHJrYYzKlao84NfrDxIbrZfGoOO0KeCz"
}
response = requests.get(url, headers=headers)
print(response.json())
