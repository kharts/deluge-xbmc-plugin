'''
Created on Mar 30, 2012

@author: Iulian Postaru
'''

from StringIO import StringIO
import gzip

def unGzip(gzipContent) :
    buf = StringIO(gzipContent)
    unz = gzip.GzipFile(fileobj=buf)
    return unz.read()
