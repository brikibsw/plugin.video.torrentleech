import urllib,urllib2,re,os
from BeautifulSoup import BeautifulSoup


base_url = 'http://thepiratebay.org/top'
req = urllib2.Request(base_url)
response = urllib2.urlopen(req)
link=response.read()
response.close()
soup = BeautifulSoup(link)
url = 'video'
if url == 'video':
		items = soup.findAll('td', attrs={'class' : "categoriesContainer"})[0]('dd')[1]('a')
elif url == 'audio':
		items = soup.findAll('td', attrs={'class' : "categoriesContainer"})[0]('dd')[0]('a')
elif url == 'apps':
		items = soup.findAll('td', attrs={'class' : "categoriesContainer"})[0]('dd')[2]('a')
elif url == 'games':
		items = soup.findAll('td', attrs={'class' : "categoriesContainer"})[1]('dd')[0]('a')
elif url == 'other':
		items = soup.findAll('td', attrs={'class' : "categoriesContainer"})[1]('dd')[1]('a')
for item in items:
		name = item['title']
		url = item['href']
		print name, url
				
