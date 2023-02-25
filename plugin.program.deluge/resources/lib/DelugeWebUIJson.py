'''
Created on Mar 29, 2012

@author: Iulian Postaru
'''

import json, urllib2
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

    #{"method":"auth.check_session","params":[],"id":1}
    def checkSession(self) :
        return self.isResultOk(self.sendReq('auth.check_session', [], self.getJsonId(), self.cookie))
    
    #{"method":"core.pause_all_torrents","params":[],"id":0}
    def pauseAllTorrents(self) :
        return self.isResultOk(self.sendReq('core.pause_all_torrents', [], self.getJsonId(), self.cookie))
    
    #{"method":"core.resume_all_torrents","params":[],"id":0}
    def resumeAllTorrents(self) :
        return self.isResultOk(self.sendReq('core.resume_all_torrents', [], self.getJsonId(), self.cookie))
    
    #{"method":"system.listMethods","params":[],"id":0}
    def listMethods(self) :
        return self.sendReq('system.listMethods', [], self.getJsonId(), self.cookie)
    #{"id":2,"method":"web.update_ui","params":[["name","state","save_path","download_payload_rate","upload_payload_rate","num_seeds","num_seeds","num_peers","total_peers","eta","total_done","total_uploaded","total_size","progress","label"],[]]}
    #{"method":"web.update_ui","params":[["queue","name","total_size","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host"],{}],"id":16}
    def updateUi(self) :
        return self.sendReq('web.update_ui', [["downloaded","queue","name","total_size","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host", "label", "total_done"],{}], self.getJsonId(), self.cookie)

    #{"method":"web.connected","params":[],"id":8}
    def connected(self) :
        return self.isResultOk(self.sendReq('web.connected', [], self.getJsonId(), self.cookie))
    
    #{"method":"web.connect","params":["9f1fdd3f2c1b2422951ac0297c3dc9fa5dbfe1e2"],"id":15}
    def connect(self, hostId) :
        return self.noError(self.sendReq('web.connect', [hostId], self.getJsonId(), self.cookie))
    
    #{"method":"web.get_hosts","params":[],"id":9}
    def getHosts(self) :
        jsonRes = self.sendReq('web.get_hosts', [], self.getJsonId(), self.cookie)
        jdata = json.loads(jsonRes)
        hosts = []
        for host in jdata['result']:
            hosts.append(host)
        return hosts
    
    #{"method":"web.get_events","params":[],"id":10}
    def getEvents(self) :
        return self.sendReq('web.get_events', [], self.getJsonId(), self.cookie)
    
    #{"method":"web.get_host_status","params":["e2b0f9c8feb2fdf08548459a38c5daef629fe7a4"],"id":11}
    # the hostId is returned by webGetHosts
    def getHostStatus(self, hostId) :
        return self.sendReq('web.get_host_status', [hostId], self.getJsonId(), self.cookie)
    
    #{"method":"core.pause_torrent","params":[["60d5d82328b4547511fdeac9bf4d0112daa0ce00"]],"id":2}
    def pauseTorrent(self, torrentId):
        return self.isResultOk(self.sendReq('core.pause_torrent', [[torrentId]], self.getJsonId(), self.cookie))
    
    #{"method":"core.resume_torrent","params":[["60d5d82328b4547511fdeac9bf4d0112daa0ce00"]],"id":2}
    def resumeTorrent(self, torrentId):
        return self.isResultOk(self.sendReq('core.resume_torrent', [[torrentId]], self.getJsonId(), self.cookie))
    
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
    
    #label.add
    
    def labelSetTorrent(self, torrentId, label):
        return self.sendReq('label.set_torrent', [torrentId, label], self.getJsonId(), self.cookie)
    
    #{"method":"web.get_torrent_files","params":["9982b1b5718279562760544e7007b765602a86ee"],"id":392}
    def getTorrentFiles(self, torrentId):
        return self.sendReq('web.get_torrent_files', [torrentId], self.getJsonId(), self.cookie)

    #   {"method":"core.set_torrent_options
    def setTorrentOptions(self, torrentId, optionName, optionValue):
        #return self.sendReq('core.set_torrent_options', [], self.getJsonId(), self.cookie)
        return self.sendReq('core.set_torrent_options', [[torrentId],{optionName:optionValue}], self.getJsonId(), self.cookie)
    
    #{"method":"web.get_events","params":[],"id":391}
    #{"method":"web.get_torrent_files","params":["9982b1b5718279562760544e7007b765602a86ee"],"id":392}
    
    
    #{"method":"label.get_labels","params":[],"id":10}
    #def getLabels(self) :
    #    return self.sendReq('label.get_labels', [], self.getJsonId(), self.cookie)
    
    #{"id":2,"method":"core.set_config","params":[[{"max_upload_speed":2},{"max_download_speed":1}]]}
    
#{"id":2,"method":"core.add_torrent_url","params":["http://btjunkie.org/torrent/Ubuntu-9-10-i386-BETA/4358b74c45dccf021307145a899c1fbaf0d60663f899/download.torrent",[]]}
    
#web.add_torrents  
#core.force_recheck
#core.set_torrent_prioritize_first_last
#core.set_torrent_move_completed
#core.set_torrent_file_priorities
#core.set_torrent_remove_at_ratio
#core.set_torrent_stop_ratio
#core.move_storage
#core.force_reannounce
#core.add_torrent_file
#core.set_torrent_move_completed_path
#core.set_torrent_stop_at_ratio
#core.rename_folder
#core.rename_files
#core.queue_top
#core.queue_down
#core.queue_up
#daemon.shutdown
#web.start_daemon
#web.stop_daemon
#webui.start
#webui.stop
#core.add_torrent_magnet
#auth.change_password
#web.get_torrent_files
