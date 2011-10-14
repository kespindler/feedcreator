#!/usr/bin/env python
import feedparser
import sys
from subprocess import Popen, PIPE, STDOUT
from urllib import urlopen
import sys

# Returns 0 if ran without output, else returns the actual output
def run(cmd, bshell = False, verbose = False):
    p = Popen(cmd, stdout = PIPE, stderr = STDOUT, shell = bshell)
    pstdout = p.communicate()[0]
    if verbose:
        if bshell:
            print cmd
        else:
            print ' '.join(cmd)
    if pstdout:
        if verbose:
            print pstdout
        return pstdout
    return 0

a = """http://gdata.youtube.com/feeds/api/users/knowitvideos/uploads?start-index={0}&alt=json&orderby=published&format=1"""

def dlvideo(url, title = None):
    print 'Downloading', title or url, '...'
    run(['yt-dl', '-t', url], False, True)

#finds items in the feed that matches query, and downloads those. Returns # of items found.
def findinfeed(feed, query):
    items = eval(feed)
    entries = items['feed']['entry']
    result = 0
    for e in entries:
        if query in e['title']['$t']:
            dlvideo(e['link'][0]['href'], e['title']['$t'])
            result += 1
    return result

def main():
    # sys.argv[1] is the unit number
    numfound = 1
    startindex = 1
    unit = sys.argv[1]
    while numfound:
        url = a.format(startindex)
        conn = urlopen(url)
        feedstring = conn.read()
        conn.close()
        numfound = findinfeed(feedstring, 'Unit {0}'.format(unit))
        startindex += 25

if __name__ == '__main__':
    main()
