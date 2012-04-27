'''
Created on Apr 27, 2012

@author: Iulian Postaru
'''

class BaseList(list):

    def __str__(self):
        strRes = ''
        for element in self:
            strRes = strRes + ';' + str(element)
        return strRes