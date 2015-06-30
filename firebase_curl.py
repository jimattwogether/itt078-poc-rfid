import httplib2
http = httplib2.Http()

body = '{"name" : "Jim"}'
url = 'https://intense-heat-9265.firebaseio.com/test.json'
headers = {}
response, content = http.request(url, 'PUT', body=body, headers=headers)

#print response
print content

response, content = http.request(url, 'GET')

#print response
print content
