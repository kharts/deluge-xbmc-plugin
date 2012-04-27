'''
Created on Apr 27, 2012

@author: Iulian Postaru
'''

class TorrentList(list):

    def finishedCount(self):
        count = 0
        for torrent in self:
            if torrent.progress == 100:
                count = count + 1
        return count
    
    def unfinishedCount(self):
        count = 0
        for torrent in self:
            if torrent.progress > 0 and torrent.progress > 100:
                count = count + 1
        return count
    
    def unstartedCount(self):
        count = 0
        for torrent in self:
            if torrent.progress == 0:
                count = count + 1
        return count