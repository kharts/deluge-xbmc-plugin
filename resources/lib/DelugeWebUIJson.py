'''
Created on Mar 29, 2012

@author: Iulian Postaru
'''

import json, urllib2, base64
from utils import unGzip

class DelugeWebUIJson(object):
    jsonid = 1
    cookie = None
    url = None

    def __init__(self, url):
        self.url = url
    
    #TODO: to add an try catch to return None when connection is unsucsessfull
    def sendReq(self, methodName, params, jsonid, cookie):
        json_dict = {'method':methodName,'params':params,'id':jsonid}
        data = json.dumps(json_dict)
        req = urllib2.Request(self.url, data, {'Content-Type': 'application/json'})
        if cookie is not None :
            req.add_header('cookie', cookie)
        res = urllib2.urlopen(req)
        DelugeWebUIJson.cookie = res.headers.get('Set-Cookie')
        encoding = res.headers.getheader('Content-Encoding')
        content = res.read()
        res.close()
        if encoding == 'gzip' :
            return unGzip(content)
        return content
    
    def getJsonId(self):
        self.jsonid += 1
        return self.jsonid
    
    def isResultOk(self, jsonRes):
        jsonData = json.loads(jsonRes)
        if jsonData['error'] == None :
            return jsonData['result']
        return False
    
    def noError(self, jsonRes):
        jsonData = json.loads(jsonRes)
        if jsonData['error'] == None :
            return True
        return False
    
    def login(self, password) :
        return self.isResultOk(self.sendReq('auth.login', [password], self.getJsonId(), None))

    def checkSession(self) :
        return self.isResultOk(self.sendReq('auth.check_session', [], self.getJsonId(), self.cookie))
    
    def pauseAllTorrents(self) :
        return self.isResultOk(self.sendReq('core.pause_all_torrents', [], self.getJsonId(), self.cookie))
    
    def resumeAllTorrents(self) :
        return self.isResultOk(self.sendReq('core.resume_all_torrents', [], self.getJsonId(), self.cookie))
    
    def listMethods(self) :
        return self.sendReq('system.listMethods', [], self.getJsonId(), self.cookie)

    def updateUi(self) :
        return self.sendReq('web.update_ui', [["downloaded","queue","name","total_size","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host", "label", "total_done"],{}], self.getJsonId(), self.cookie)

    def connected(self) :
        return self.isResultOk(self.sendReq('web.connected', [], self.getJsonId(), self.cookie))
    
    def connect(self, hostId) :
        return self.noError(self.sendReq('web.connect', [hostId], self.getJsonId(), self.cookie))
    
    def getHosts(self) :
        jsonRes = self.sendReq('web.get_hosts', [], self.getJsonId(), self.cookie)
        jdata = json.loads(jsonRes)
        hosts = []
        for host in jdata['result']:
            hosts.append(host)
        return hosts
    
    def getEvents(self) :
        return self.sendReq('web.get_events', [], self.getJsonId(), self.cookie)
    
    # the hostId is returned by webGetHosts
    def getHostStatus(self, hostId) :
        return self.sendReq('web.get_host_status', [hostId], self.getJsonId(), self.cookie)
    
    def pauseTorrent(self, torrentId):
        return self.isResultOk(self.sendReq('core.pause_torrent', [[torrentId]], self.getJsonId(), self.cookie))
    
    def resumeTorrent(self, torrentId):
        return self.isResultOk(self.sendReq('core.resume_torrent', [[torrentId]], self.getJsonId(), self.cookie))
    
    def addTorrent(self, torrentUrl):
        if torrentUrl.startswith("magnet:"):
            jsonRes = self.sendReq('core.add_torrent_magnet', [torrentUrl, {}], self.getJsonId(), self.cookie)
        else:
            metaInfo = base64.b64encode(urllib2.urlopen(torrentUrl).read())
            jsonRes = self.sendReq('core.add_torrent_file', ["", metaInfo, {}], self.getJsonId(), self.cookie)
        return self.isResultOk(jsonRes)

    #TODO: is not working, to find out the params which should be passed
    #{"method":"core.remove_torrent","params":["60d5d82328b4547511fdeac9bf4d0112daa0ce00", false],"id":2}
    #{"method":"core.remove_torrent","params":[["60d5d82328b4547511fdeac9bf4d0112daa0ce00"],false],"id":2}
    def removeTorrent(self, torrentId, removeData):
        return self.sendReq('core.remove_torrent', [torrentId,removeData], self.getJsonId(), self.cookie)
    
    def getLabels(self):
        jsonRes = self.sendReq('label.get_labels', [], self.getJsonId(), self.cookie)
        jdata = json.loads(jsonRes)
        labels = []
        if jdata['result']:
            for label in jdata['result']:
                labels.append(label)
        return labels
    
    def labelSetTorrent(self, torrentId, label):
        return self.sendReq('label.set_torrent', [torrentId, label], self.getJsonId(), self.cookie)
    
    def getTorrentFiles(self, torrentId):
        return self.sendReq('web.get_torrent_files', [torrentId], self.getJsonId(), self.cookie)

    def setTorrentOptions(self, torrentId, optionName, optionValue):
        return self.sendReq('core.set_torrent_options', [[torrentId],{optionName:optionValue}], self.getJsonId(), self.cookie)