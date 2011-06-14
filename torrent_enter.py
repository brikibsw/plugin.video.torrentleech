resp1 = opener.open('http://www.torrentleech.org/torrents/browse/index/categories/10,11,13,14')
var2 = resp1.read()
var3 = re.findall(re.compile('<td class="name"><span class="title"><a href="/torrent/(.+?)">'), var2)
listIterator = []
listIterator[:] = range(0, 10)
for i in listIterator:
    opentorrent = opener.open('http://www.torrentleech.org/torrent/'+var3[i])
    readtorrent = opentorrent.read()
    torrentname = re.findall(re.compile('<td class="label">Torrent Name</td><td>(.+?)</td>'), readtorrent)
    print torrentname, var3[i]