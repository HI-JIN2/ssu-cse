"""
1. (3 points) Write a Python script for demonstrating "Raw Network Conversation." 
Use the socket library to request ip-api JSON endpoint(https://ip-api.com/docs/api:json) 
to GET your IP Geolocation such as city, regionName, country, lat, lon.

parameters = {'fields':'city,regionName,country,lat,lon', 'lang':'fr'}

Hint: Take a reference from Chapter 1, Listing 1-4 (search.py) 
Note: Don't use any other library(such as requests,http.client, etc.) for an API request
"""


import socket, json


# Construct the HTTP request message
request_text = "GET /json/?fields=city,regionName,country,lat,lon&lang=fr HTTP/1.1\r\nHost: " + "\r\n\r\n"

# Create a socket object and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host 'ip-api.com', port 80
sock.connect(('ip-api.com', 80))

# Send the request message to the server
sock.send(request_text.encode())

# Receive the response message from the server
response = b""
while True:
    data = sock.recv(4096)
    if not data:
        break
    response += data

# Decode the response message and extract the relevant data
response = response.decode().split('\r\n\r\n')[1]
data = json.loads(response)

# Print the relevant data
print("city:", data['city'])
print("regionName:", data['regionName'])
print("country:", data['country'])
print("lat:", data['lat'])
print("lon:", data['lon'])

# Close the socket
sock.close()
