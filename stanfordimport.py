#!/usr/bin/env python
#The way to use this script is as follows:
#Execute ./stanfordimport.py {0}, where {0} is the course unit of the videos
#you'd like to download. This script then starts at the most recent videos in
#the stanford lecture's youtube feed, and goes back in time to find videos
#of that course unit. It downloads metadata about 25 videos at a time, and will
#stop requesting metadata once it receives a set of 25 where it finds NO videos
#from a given unit, on the assumption that we've got too far back in time at that
#point. Note that there is a guard to prevent this stop until you've found _any_
#videos, so if you try to download Unit 2 while the course is on Unit 7, that should
#work fine.
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
    if not 'entry' in items['feed']:
        print 'No entries in this feed'
        return 0
    entries = items['feed']['entry']
    result = 0
    for e in entries:
        if query in e['title']['$t']:
            dlvideo(e['link'][0]['href'], e['title']['$t'])
            result += 1
    return result

def main():
    # sys.argv[1] is the unit number
    numfound = 0
    foundany = False
    startindex = 1
    unit = sys.argv[1]
    while numfound or not foundany:
        url = a.format(startindex)
        conn = urlopen(url)
        feedstring = conn.read()
        conn.close()
        numfound += findinfeed(feedstring, 'Unit {0}'.format(unit))
        if numfound:
            foundany = True
        startindex += 25
    if numfound:
        print 'Downloaded', numfound, 'videos.'
    else:
        print 'Could not find any videos for the unit. Something went wrong.'

if __name__ == '__main__':
    main()
