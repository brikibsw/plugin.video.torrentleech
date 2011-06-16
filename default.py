import string, urllib2, urllib, re, cookielib, xbmc, xbmcgui, xbmcplugin, sys, os, traceback, xbmcaddon, string, threading
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.torrentleech')

username = __settings__.getSetting('username')
user_password = __settings__.getSetting('user_password')
downloadPath = __settings__.getSetting('downloadPath')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
exitFlag = 0
currentPage = 0
print 'downloadPath: ' + downloadPath

def Categories():
		addDir('Video HD','video_hd',1,'http://static2.torrentleech.org/images/categories/13.png')
		addDir('Video BRrip','video_brrip',1,'http://static2.torrentleech.org/images/categories/14.png')
		addDir('Video DVDrip','video_dvdrip',1,'http://static2.torrentleech.org/images/categories/10.png')
		
def mesnotloged(self):
	dialog = xbmcgui.Dialog()
	dialog.ok(" Error", " You are not looged in ")

def mesloged(self):
	dialog = xbmcgui.Dialog()
	dialog.ok(" Wellcome back "+username, " You are looged in ")
	
def downloaded(self):
	dialog = xbmcgui.Dialog()
	dialog.ok(" Torrent has been", " downloaded ")
		
def getSubcate(url):
		if url == 'video_hd':
				url = 'http://www.torrentleech.org/torrents/browse/index/categories/13'
				resp1 = opener.open(url)
				var2 = resp1.read()
				soup = BeautifulSoup(var2)
				for item in soup.findAll('td', attrs={'class' : "quickdownload"}):
					links=item.findAll('a')
					link = re.findall(re.compile('<a href="/download/(.+?)"><img src="(.+?)".+?/></a>'), '['+str(links)+']')
					for ilink in link:
						ilink1 = str(ilink).split(',')
						t = str(ilink[0]).split('/')
						tid = t[0]
						name = t[1]
						icon = 'http://static2.torrentleech.org/images/categories/13.png'
						url = tid
						addDir(name,url,4,icon)
		elif url == 'video_brrip':
				url = 'http://www.torrentleech.org/torrents/browse/index/categories/14'
				resp1 = opener.open(url)
				var2 = resp1.read()
				soup = BeautifulSoup(var2)
				for item in soup.findAll('td', attrs={'class' : "quickdownload"}):
					links=item.findAll('a')
					link = re.findall(re.compile('<a href="/download/(.+?)"><img src="(.+?)".+?/></a>'), '['+str(links)+']')
					for ilink in link:
						ilink1 = str(ilink).split(',')
						t = str(ilink[0]).split('/')
						tid = t[0]
						name = t[1]
						icon = 'http://static2.torrentleech.org/images/categories/14.png'
						url = tid
						addDir(name,url,4,icon)
		elif url == 'video_dvdrip':
				url = 'http://www.torrentleech.org/torrents/browse/index/categories/10'
				resp1 = opener.open(url)
				var2 = resp1.read()
				soup = BeautifulSoup(var2)
				for item in soup.findAll('td', attrs={'class' : "quickdownload"}):
					links=item.findAll('a')
					link = re.findall(re.compile('<a href="/download/(.+?)"><img src="(.+?)".+?/></a>'), '['+str(links)+']')
					for ilink in link:
						ilink1 = str(ilink).split(',')
						t = str(ilink[0]).split('/')
						tid = t[0]
						name = t[1]
						icon = 'http://static2.torrentleech.org/images/categories/10.png'
						url = tid
						addDir(name,url,4,icon)

def DOWN(name,url):
	torrent_url = 'http://www.torrentleech.org/download/'+url+'/'+name
	torrent_name = name
	print torrent_name
	print torrent_url
	torrent_file = urllib2.urlopen(torrent_url)
	output = open(downloadPath+torrent_name,'wb')
	output.write(torrent_file.read())
	output.close()
	downloaded('')
	
def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]
								
		return param

def addDir(name,url,mode,iconimage):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
			
params=get_params()
url=None
name=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

if mode==None or mode==1 or mode==2 or mode==3 or mode==4:
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	resp = opener.open('http://www.torrentleech.org')
	lol = 'submit'
	data = urllib.urlencode({'username':username,'password':user_password,'login':lol})
	resp = opener.open('http://www.torrentleech.org/user/account/login', data)
	var1 = resp.read()
	resp.close()
	loged = re.findall(re.compile('<span class="memberbar_alt">(.+?)</span>'), var1)
	if len(loged)<=0 and mode==None:
		mesnotloged('')
	elif len(loged)>0 and mode==None:
		mesloged('')

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
		print ""
		Categories()
		
elif mode==1:
		print""
		getSubcate(url)
		
elif mode==2:
		print""
		getTorrents(url)
		
elif mode==3:
		print""
		DOWNLOAD(url)
		
elif mode==4:
		print""
		DOWN(name,url)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))