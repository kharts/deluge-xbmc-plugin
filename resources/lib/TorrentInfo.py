'''
Created on Apr 10, 2012

@author: Iulian Postaru
'''

class TorrentInfo(object):

    def __init__(self):
        '''
        Constructor
        '''

    torrentId = None
    label = None
    name = None
    progress = 0.0
    ratio = -1.0
    state = None
    timeAdded = None
    totalDone = None
    totalSeeds = 0
    totalSize = 0
    trackerHost = None
    downloadPayloadRate = 0
    uploadPayloadRate = 0
    eta = 0
    
    def getStrSize(self):
        size = int(self.totalSize) / (1024*1024)
        if (size >= 1024.00):
            size_str = str(round(size / 1024.00,2)) +"Gb"
        else:
            size_str = str(size) + "Mb"
        return size_str


    #TODO: to add a zero before in case hours or minutes are only from one digit
    def getStrEta(self):
        remain = self.eta / 60
        if (remain >= 60):
            remain_str = str(remain//60) + ':' + str(remain%60)
        elif(remain == -1):
            remain_str = '--:--'
        else:
            remain_str = '00:' + str(remain)
        return remain_str
    
    def __str__(self):
        return self.name;