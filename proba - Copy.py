import urllib, urllib2, cookielib, re
from BeautifulSoup import BeautifulSoup

username = ''
user_password = ''


cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
resp = opener.open('http://www.torrentleech.org')
lol = 'submit'
data = urllib.urlencode({'username':username,'password':user_password,'login':lol})
resp = opener.open('http://www.torrentleech.org/user/account/login', data)
var1 = resp.read()
resp.close()


resp1 = opener.open('http://www.torrentleech.org/torrents/browse/index/categories/10,11,13,14')
var2 = resp1.read()

var3 = re.findall(re.compile('<td class="name"><span class="title"><a href="/torrent/(.+?)">(.+?)</a>'), var2)
listIterator = []
listIterator[:] = range(0, 10)
for i in listIterator:
    print var3[i]
    print("\n")










