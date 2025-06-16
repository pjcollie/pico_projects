import urequests

# Test internet by querying a webpage
print("Querying google.com:")
response = urequests.get("http://www.google.com")
print(response.content)
response.close()

# Query current time from a server
print("\nQuerying current GMT+0 time:")
response = urequests.get("http://date.jsontest.com")
print(response.json())
