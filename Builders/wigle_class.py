

#Need to run setup script to ensure you have wigle installed
import os
import wigle


def Get_AP(username, password, ssid):
   w = wigle.Wigle(username, password)
   result = w.search(ssid=ssid)
   print result

if __name__ == "__main__":
   Get_AP('offtest', '83128312','foobar1234')


"""
POST /jsonLogin?noexpire=off&destination=%2F&credential_0=offtest&credential_1=83128312 HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Accept-Encoding: identity, deflate, compress, gzip
Accept: application/json, text/javascript
User-Agent: python wigle client

HTTP/1.0 501 Unsupported method ('POST')
Server: SimpleHTTP/0.6 Python/2.7.3
Date: Tue, 02 Jun 2015 18:11:07 GMT
Content-Type: text/html
Connection: close

<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code 501.
<p>Message: Unsupported method ('POST').
<p>Error code explanation: 501 = Server does not support this operation.
</body>
"""


https://wigle.net/api/v1/jsonSearch?ssid=foobar1234
https://wigle.net/api/v1//jsonLogin?noexpire=off&destination=%2F&credential_0=offtest&credential_1=83128312