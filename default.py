import urllib,urllib2,re,os, cookielib
import xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.torrentleech')

username = __settings__.getSetting('username')
user_password = __settings__.getSetting('user_password')
downloadPath = __settings__.getSetting('downloadPath')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )

def Categories():
		addDir('Video SD','video_sd',1,icon)
		addDir('Audio HD','video_hd',1,icon)
		addDir('Search','',4,icon)


def getSubcate(url):
		url = '13,14'
		name = 'HD'
		addDir('New Videos- '+name,'http://www.torrentleech.org/torrents/browse/index/categories/'+url,2,icon)

def getTorrents(url):
		resp1 = opener.open(url)
		var2 = resp1.read()
		var3 = re.findall(re.compile('<td class="name"><span class="title"><a href="/torrent/(.+?)">(.+?)</a>'), var2)
		listIterator = []
		listIterator[:] = range(0, 10)
		for i in listIterator:
			print var3[i][1]
			try:
					name = var3[i][1]
					url = 'http://www.torrentleech.org/torrent/'+var3[i][0]
					addDir(name,url,3,'')
			except:
					pass

def showTorrent(name,url):
		cj = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		opentorrent = opener.open(url)
		readtorrent = opentorrent.read()
		icon = re.findall(re.compile('<td class="label">Torrent Name</td><td>(.+?)</td></tr>'), readtorrent)
		print icon
		addDir(name,url,3,'http://static.torrentleech.org/images/covers/MV5BMTE5OTQzMzU3Nl5BMl5BanBnXkFtZTcwNTA3MTMyMQ@@._V1__1787197454.jpg')
		
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
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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

if mode==2:
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	resp = opener.open('http://www.torrentleech.org')
	lol = 'submit'
	data = urllib.urlencode({'username':username,'password':user_password,'login':lol})
	resp = opener.open('http://www.torrentleech.org/user/account/login', data)
	var1 = resp.read()
	resp.close()

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
		showTorrent(name,url)
		
elif mode==4:
		print""
		Search()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
