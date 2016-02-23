

import io
import json
import urllib

url = 'http://octopart.com/api/v3/parts/match?'
url += '&queries=[{"mpn":"MMSD-20-26-L-40.00-S-K-M"}]'
url += '&apikey=ab07571e'
url += '&pretty_print=true'


data = urllib.urlopen(url).read()
with io.open('data.txt', 'w', encoding='utf-8') as f:
    f.write(unicode(data))

response = json.loads(data)

print(response)

# print request time (in milliseconds)
#print(response['msec'])

# print mpn's
for result in response['results']:
    for item in result['items']:
        print(item['mpn'])

