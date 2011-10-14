#!/usr/bin/env python
import feedparser
import sys
from subprocess import Popen, PIPE, STDOUT
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

def download(url):
    feed = feedparser.parse(url)
    for item in feed['items']:
        print 'Downloading', item['title'], '...'
        run(['yt-dl', '-t', item['link']], False, True)

def main():
    download(sys.argv[1])

if __name__ == '__main__':
    main()
