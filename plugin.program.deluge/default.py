import urllib, sys, os, re, time
import xbmcaddon, xbmcplugin, xbmcgui, xbmc

# Plugin constants 
__addonname__ = "DelugeXBMCPlugin"
__addonid__   = "plugin.program.deluge"
__addon__     = xbmcaddon.Addon(id=__addonid__)
__language__  = __addon__.getLocalizedString
__cwd__       = xbmc.translatePath( __addon__.getAddonInfo('path') )
__profile__   = xbmc.translatePath( __addon__.getAddonInfo('profile') )
__icondir__   = os.path.join( __cwd__,'resources','icons' )

# Shared resources 
BASE_RESOURCE_PATH = os.path.join( __cwd__, 'resources', 'lib' )
sys.path.append (BASE_RESOURCE_PATH)

UT_ADDRESS = __addon__.getSetting('ip')
UT_PORT = __addon__.getSetting('port')
UT_PASSWORD = __addon__.getSetting('pwd')

url = 'http://' + UT_ADDRESS + ':' + UT_PORT + '/json'
baseurl = url

from utilities import *
import json
from DelugeWebUI import DelugeWebUI

webUI = DelugeWebUI(url)

def updateList():
	restoreSession()
	return webUI.getTorrentList()

def listTorrents(filter):
	torrentList = updateList()
	mode = 1
	for torrentInfo in torrentList:
		xbmc.log( 'state='+torrentInfo.state, xbmc.LOGINFO )
		xbmc.log( 'label='+torrentInfo.label, xbmc.LOGINFO )
		if torrentInfo.state == filter or filter == 'All' or ((torrentInfo.state == 'Downloading' or torrentInfo.state == 'Seeding') and filter == 'Active') or torrentInfo.label == filter:
			if torrentInfo.state == 'Paused':
				thumb = os.path.join(__icondir__,'pause.png')
			elif torrentInfo.state == 'Downloading':
				thumb = os.path.join(__icondir__,'play.png')
			elif torrentInfo.state == 'Queued':
				thumb = os.path.join(__icondir__,'queued.png')
			else:
				thumb = os.path.join(__icondir__,'unknown.png')
			url = baseurl
			xbmc.log( 'url='+url, xbmc.LOGDEBUG )
			addTorrent(torrentInfo.name+" "+__language__(30001)+str(torrentInfo.progress)+"% "+__language__(30002)+torrentInfo.getStrSize()+" "+__language__(30003)+ str(torrentInfo.downloadPayloadRate)+"Kb/s "+__language__(30004)+str(torrentInfo.uploadPayloadRate)+"Kb/s "+__language__(30005)+torrentInfo.getStrEta(),url,mode,thumb,torrentInfo.torrentId)
			mode = mode + 1
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)

def performAction(selection):
	restoreSession()
	dialog = xbmcgui.Dialog()
	sel = dialog.select(__language__(32001),[__language__(32011),__language__(32012),__language__(32002),__language__(32003),__language__(32007),__language__(32008),__language__(32019)])
	if sel == 0:
		webUI.pauseAllTorrents()
	if sel == 1:
		webUI.resumeAllTorrents()
	if sel == 2:
		webUI.pauseTorrent(selection)
	if sel == 3:
		webUI.resumeTorrent(selection)
	if sel == 4:
		webUI.removeTorrent(selection, True)
	if sel == 5:
		webUI.removeTorrent(selection, True)
	if sel == 6:
		labels = webUI.getLabels()
		labelDialog = dialog.select(__language__(32020), labels)
		webUI.labelSetTorrent(selection, labels[labelDialog])
	xbmc.executebuiltin('Container.Refresh')

def restoreSession():
	try:
		if webUI.checkSession() == False:
			if webUI.login(UT_PASSWORD):
				if not webUI.connected():
					webUI.connectToFirstHost()
	except urllib2.URLError:
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(__addonname__ + ' ' + __language__(32100).encode('utf8'), __language__(32101).encode('utf8'), __language__(32102).encode('utf8'))
		if ret == True:
			__addon__.openSettings()
		sys.exit()
	
def pauseAll():
	restoreSession()
	webUI.pauseAllTorrents()
	xbmc.executebuiltin('Container.Refresh')

def resumeAll():
	restoreSession()
	webUI.resumeAllTorrents()
	xbmc.executebuiltin('Container.Refresh')
    
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

def addTorrent(name,url,mode,iconimage,hashNum):
    xbmc.log( 'mode='+str(mode), xbmc.LOGINFO )
    xbmc.log( 'url='+url, xbmc.LOGINFO )
    xbmc.log( DelugeWebUI.cookie, xbmc.LOGINFO )
    xbmc.log( webUI.cookie, xbmc.LOGINFO )
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&hashNum="+str(hashNum)
    ok = True
    point = xbmcgui.ListItem(name,thumbnailImage=iconimage)
    rp = "XBMC.RunPlugin(%s?mode=%s)"
    point.addContextMenuItems([(__language__(32011), rp % (sys.argv[0], 1000)),(__language__(32012), rp % (sys.argv[0], 1001))],replaceItems=True)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=point,isFolder=False)
	
def addFilters(filter,url,mode,iconimage):
	if filter.name == '':
		displayName = __language__(30009) + '(' + str(filter.count) + ')'
	else:
		displayName = str(filter)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(filter.name)
	ok=True
	liz=xbmcgui.ListItem(displayName, iconImage="DefaultFolder.png",thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": displayName })
	rp = "XBMC.RunPlugin(%s?mode=%s)"
	liz.addContextMenuItems([(__language__(32011), rp % (sys.argv[0], 1000)),(__language__(32012), rp % (sys.argv[0], 1001))],replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

def listStateFilters():
	restoreSession()
	filters = webUI.getStateFilters()
	for filter in filters:
		if filter.count > 0:
			addFilters(filter,'',7007,'')
	
	filters = webUI.getLabelsFilters()
	for filter in filters:
		if filter.count > 0:
			addFilters(filter,'',7007,'')
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)


params = get_params()
url = None
name = None
mode = 0
hashNum = None

try:
    url = urllib.unquote_plus(params['url'])
except:
    pass
try:
    name = urllib.unquote_plus(params['name'])
except:
    pass
try:
    mode = int(params['mode'])
except:
    pass
try:
    hashNum = urllib.unquote_plus(params['hashNum'])
except:
    pass

if mode == 0:
    listStateFilters()
	
if mode == 7007:
	listTorrents(name)

elif mode == 1000:
    pauseAll()

elif mode == 1001:
    resumeAll()

elif mode == 1004:
    limitSpeeds()

#elif mode == 1005:
#    addFiles()

elif 0 < mode < 1000:
    performAction(hashNum)

