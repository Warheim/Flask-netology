import requests


# response = requests.post('http://127.0.0.1:5000/users/',
#                          json={'email': 'some@email.com', 'password': '123'})

response = requests.get('http://127.0.0.1:5000/users/1')

print(response.status_code)
print(response.json())
