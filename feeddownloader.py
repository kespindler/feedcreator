#!/usr/bin/env python
import feedparser
http://www.youtube.com/watch?v=BnIJ7Ba5Sr4&feature=youtube_gdata
import sys
import codecs
import re
import os
import optparse
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
        run(['yt-dl', '-t', item['link']], False, True)
