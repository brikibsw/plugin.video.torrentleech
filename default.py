import string, urllib2, urllib, re, cookielib, xbmc, xbmcgui, xbmcplugin, sys, os, traceback, xbmcaddon, string, threading

__settings__ = xbmcaddon.Addon(id='plugin.video.hdbits')

username = __settings__.getSetting('username')
user_password = __settings__.getSetting('user_password')
downloadPath = __settings__.getSetting('downloadPath')
exitFlag = 0
currentPage = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, tmdbid, url, mode, iconimage):
        print "starting thread: " + str(threadID)
        self.threadID = threadID
        self.title = name
        self.tmdbid = tmdbid
        self.url = url
        self.mode = mode
        self.iconimage = iconimage
        threading.Thread.__init__(self)
    def run(self):
        print "Starting " + str(self.threadID)
        print "adding link for thread: " + str(self.threadID)
        addLink(self.title, self.tmdbid, self.url, self.mode, self.iconimage, self.threadID)
        print "added link for thread: " + str(self.threadID)
        print "Exiting " + str(self.threadID)

if ( not __settings__.getSetting( 'firstrun' ) ):
    __settings__.openSettings()
    __settings__.setSetting( 'firstrun', '1' )

print 'downloadPath: ' + downloadPath

def addLink(name,tmdbid,url,mode,iconimage,no):
    try:
        tmdb = 'http://api.themoviedb.org/2.1/Movie.imdbLookup/en/xml/6b6effafe7c0b6fa17191d0430f546f8/tt' + tmdbid
        resp = opener.open(tmdb)
        svar3 = resp.read()
        resp.close()
        poster = re.compile('<image type="poster" url="(.+?)" size="original"').findall(svar3)
        plot = re.compile('<overview>(.+?)</overview>').findall(svar3)
        fanart = re.compile('<image type="backdrop" url="(.+?)" size="original"').findall(svar3)
        released = re.compile('<released>(.+?)</released>').findall(svar3)
    except:
        pass
    try:
        year = int(str(released[0])[0:4])
    except:
        pass
    try:
        runtime = re.compile('<runtime>(.+?)</runtime>').findall(svar3)
        rating = re.compile('<rating>(.+?)</rating>').findall(svar3)
        votes = re.compile('<votes>(.+?)</votes>').findall(svar3)
        genres = re.compile('<category type="genre" name="(.+?)" url=').findall(svar3)
        for i in range(0, len(genres)):
            if(i == 0):
                genre = genres[0]
            else:
                genre = genre + ' / ' + genres[i]
    except:
        pass
    u = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode='+str(mode) + '&name=' +urllib.quote_plus(name)
    ok = True
    try:
        cover=poster[0]
    except:
        cover=iconimage
    liz=xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=cover)
    try:
        liz.setInfo(type='Video',infoLabels={'Title': name})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'size': no})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'plot':plot[0]})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'rating': float(rating[0])})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'year': year})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'Duration': runtime[0]})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'votes': votes[0]})
    except:
        pass
    try:
        liz.setInfo(type='Video',infoLabels={'genre': genre})
    except:
        pass
    try:
        liz.setProperty('Fanart_Image',fanart[0])
    except:
        pass
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=25)
    return ok

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+'?url='+urllib.quote_plus(url)+'&mode='+str(mode)+'&name='+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage='DefaultFolder.png',thumbnailImage=iconimage)
    liz.setInfo( type='Video', infoLabels={ 'Title': name })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=3)
    return ok

def getUserInput(self, title = "Input", default="", hidden=False):
    result = None
    if not default:
	default = ""
    keyboard = xbmc.Keyboard(default, title)
    keyboard.setHiddenInput(hidden)
    keyboard.doModal()    	
    if keyboard.isConfirmed():
    	result = keyboard.getText()
    result = string.replace(result, " ", "+")
    return result


def CATEGORIES():
    addDir('Ordered by amount of leechers','http://hdbits.org/browse.php?c1=1&co1=1&m3=1&page=0&sort=leechers&h=11&d=DESC',1,'')
    addDir("Ordered by amount of seeders",'http://hdbits.org/browse.php?c1=1&co1=1&m3=1&sort=seeders&h=10&d=DESC',1,'')
    addDir("Ordered by date added",'https://hdbits.org/browse.php?c1=1&co1=1&m3=1&incldead=0&descriptions=0&from=&to=&imdbgt=0&imdblt=10&uppedby=&imdb=&search=',1,'')
    addDir("Search",'http://hdbits.org/browse.php?search=',3,'')

def DOWNLOAD():
    url=urllib.unquote_plus(params['url'])
    name=urllib.unquote_plus(params['name'])
    resp = opener.open(url)
    svar4 = resp.read()
    resp.close()
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanfilename = ''.join(c for c in name if c in valid_chars)
    torrent_filename = downloadPath + '/' + cleanfilename + '.torrent'
    torrent_file = open(torrent_filename, 'wb')
    torrent_file.write(svar4)
    torrent_file.close()

def CompileInfo(info):
    movies = ['null']*4
    try:
        movies[0] = str('https://hdbits.org/download.php?id=' + str(re.compile('p\?id=(.+?)&amp;').findall(info)[0]))
    except:
        print "error with first step"
    try:
        movies[1] = str(re.compile('&amp;hit=1">(.+?)</a>').findall(info)[0])
    except:
        print "error with second step"
    try:
        movies[3] = str(re.compile('<a href="http://www\.imdb\.com/title/tt(.+?)/">IMDB').findall(info)[0])
    except:
        print "error with third step"
    return movies

def TORRENTS(url):
    movies = [['null']*4 for i in range(30)]
    print 'three'
    resp = opener.open(url)
    print 'four'
    svar2 = resp.read()
    resp.close()
    items = re.compile('<div class=".+?"></div></td><td><b><a.+?href="details\.ph(.+?)</td>').findall(svar2)
    
    for i in items:
        print i
    
    i = 0

    while i < len(items):
        item = CompileInfo(items[i])
        i=i+1
        trad = myThread(i,item[1], item[3], item[0], 2, item[2])
        trad.start()
        
    for thread in threading.enumerate():
        if thread is not threading.currentThread():
            thread.join()
                
    nextUrl = url + "&page=" + str(currentPage + 1)
       
    addDir("Next Page",nextUrl,4,'')
        
        
url=None
name=None
mode=None

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

params = get_params();

try:
        url=urllib.unquote_plus(params['url'])
except:
        pass
try:
        name=urllib.unquote_plus(params['name'])
except:
        pass
try:
        mode=int(params['mode'])
except:
        pass

if mode==1 or mode==2 or mode==3 or mode==4:
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    print 'start'
    urllib2.install_opener(opener)
    print 'one'
    resp = opener.open('http://www.torrentleech.org')
    print 'two'    
    svar3 = resp.read()
    resp.close()
    lols = re.compile('<input type="hidden" name="lol" value="(.+?)" />').findall(svar3)
    if len(lols) == 1:
        lol = str(lols[0])
        data = urllib.urlencode({'username':username,'&password':user_password,'&login=submit'})
        resp = opener.open('http://www.torrentleech.org/user/account/login/','POST', data)
        svar1 = resp.read()
        resp.close()

if mode==3:
    print 'url before: ' + url
    url = url + getUserInput('Enter Searchstring', '')
    print 'url after: ' + url

if mode==4:
    currentPage += 1

if mode==2 or mode==3:
    currentPage = 0

if mode==None or url==None or len(url)<1:
        CATEGORIES()
 
elif mode==1 or mode==3 or mode==4:
        TORRENTS(url)
        
elif mode==2:
        DOWNLOAD()

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_SIZE)
xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
