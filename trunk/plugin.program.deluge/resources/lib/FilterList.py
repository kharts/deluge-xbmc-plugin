'''
Created on Apr 24, 2012

@author: Iulian Postaru
'''

class FilterList(list):
    
    def indexByName(self, name):
        for element in self:
            if element.name == name:
                return self.index(element)
            
    def append(self, element):
        pos = self.indexByName(element.name)
        if pos == None:
            super(FilterList, self).append(element)
        else:
            self[pos].count += 1