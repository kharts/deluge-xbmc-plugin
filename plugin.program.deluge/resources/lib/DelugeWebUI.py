'''
Created on Mar 30, 2012

@author: Iulian Postaru
'''

from DelugeWebUIJson import DelugeWebUIJson
from TorrentInfo import TorrentInfo
from Filter import Filter
from FilterList import FilterList
from TorrentList import TorrentList
import json

class DelugeWebUI(DelugeWebUIJson):
        
    def getTorrentList(self):
        torrentList = TorrentList()
        jsonRes = self.updateUi()
        jdata = json.loads(jsonRes)
        for torrentId in jdata['result']['torrents']:
            torrentInfo = TorrentInfo()
            jsonTorrentInfo = jdata['result']['torrents'][torrentId]
            torrentInfo.torrentId = torrentId
            torrentInfo.state = jsonTorrentInfo['state']
            torrentInfo.name = jsonTorrentInfo['name'].encode('utf8')
            torrentInfo.progress = int(jsonTorrentInfo['progress'])
            torrentInfo.totalSize = int(jsonTorrentInfo['total_size'])
            torrentInfo.uploadPayloadRate = round(float(jsonTorrentInfo['upload_payload_rate']) / (1024), 2)
            torrentInfo.downloadPayloadRate = round(float(jsonTorrentInfo['download_payload_rate']) / (1024), 2)
            torrentInfo.eta = int(jsonTorrentInfo['eta'])
            torrentInfo.label = jsonTorrentInfo['label']
            torrentList.append(torrentInfo)
        return torrentList
    
    def getTorrentListByLabel(self, labelName):
        torrentInfoList = self.getTorrentList()
        resultTorrentInfoList = TorrentList()
        for torrentInfo in torrentInfoList:
            if torrentInfo.label == labelName:
                resultTorrentInfoList.append(torrentInfo)
        return resultTorrentInfoList
    
    def getTorrentListByState(self, stateName):
        torrentInfoList = self.getTorrentList()
        resultTorrentInfoList = TorrentList()
        for torrentInfo in torrentInfoList:
            if torrentInfo.state == stateName:
                resultTorrentInfoList.append(torrentInfo)
        return resultTorrentInfoList
    
    def getLabelList(self, torrentList):
        labels = FilterList()
        for torrent in torrentList:
            labels.append(Filter(torrent.label, 1))
        return labels
    
    def getStateList(self, torrentList):
        states = FilterList()
        
        if len(torrentList) > 0:
            states.append(Filter('All', len(torrentList)))
        
        for torrent in torrentList:
            states.append(Filter(torrent.state, 1))
        
        finishedCount = torrentList.finishedCount()
        if finishedCount > 0:
            states.append(Filter('Finished', finishedCount))
        
        unfinishedCount = torrentList.unfinishedCount()
        if unfinishedCount > 0:
            states.append(Filter('Unfinished', unfinishedCount))
        
        unstartedCount = torrentList.unstartedCount()
        if unstartedCount > 0:
            states.append(Filter('Unstarted', unstartedCount))
        
        return states

    def getFilters(self,filterType):
        jsonRes = self.updateUi()
        jdata = json.loads(jsonRes)
        filterList = []
        for strFilter in jdata['result']['filters'][filterType]:
            filterList.append(Filter(strFilter[0], int(strFilter[1])))
        return filterList
    
    def getStateFilters(self):
        return self.getFilters('state')

    def getLabelsFilters(self):
        return self.getFilters('label')
    
    def getTrackerHostFilters(self):
        return self.getFilters('tracker_host')
    
    def connectToFirstHost(self):
        hosts = self.getHosts()
        if len(hosts) > 0:
            firstHostId = hosts[0][0]
            if self.isHostOnline(firstHostId):
                return self.connect(firstHostId)
        return False

    def isHostOnline(self, hostId):
        jsonRes = self.getHostStatus(hostId)
        jdata = json.loads(jsonRes)
        if jdata['result'][3] == 'Online':
            return True
        return False
