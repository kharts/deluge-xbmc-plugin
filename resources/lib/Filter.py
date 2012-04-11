'''
Created on Apr 10, 2012

@author: iulian.postaru
'''

class Filter(object):
    
    name = ''
    count = 0

    def __init__(self, name, count):
        self.name = name
        self.count = count
        #if (self.name == ''):
        #    self.name = 'No Label'
        
    def __str__(self):
        return str(self.name) + '(' + str(self.count) + ')'