#!/usr/bin/env python
import os.path
import os
import optparse
mime_mapping = {'.mp3': 'audio/mpeg', '.m4a': 'audio/x-m4a', '.mp4': 'video/mp4', '.m4v': 'video/x-m4v', 
                '.mov': 'video/quicktime', '.pdf': 'application/pdf', '.epub': 'document/x-epub'}

def createbase(title = '', link = '', copyright = '', subtitle = '', author = '', summary = '', description = '', 
               ownername = '', owneremail = '', imageurl = '', category = '', subcategory = '', items = ''):
    base = ['<?xml version="1.0" encoding="UTF-8"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"><channel>']
    base.append('<title>{0}</title>'.format(title))
    if link:
        base.append('<link>{0}</link>'.format(link))
    base.append('<language>en-us</language>')
    if copyright:
        base.append('<copyright>{0}</copyright>'.format(copyright))
    if subtitle:
        base.append('<itunes:subtitle>{0}</itunes:subtitle>'.format(subtitle))
    if author:
        base.append('<itunes:author>{0}</itunes:author>'.format(author))
    if summary:
        base.append('<itunes:summary>{0}</itunes:summary>'.format(summary))
    if description:
        base.append('<description>{0}</description>'.format(description))
    if ownername or owneremail:
        base.append('<itunes:owner>')
        if ownername:
            base.append('<itunes:name>{0}</itunes:name>'.format(ownername))
        if owneremail:
            base.append('<itunes:email>{0}</itunes:email>'.format(owneremail))
        base.append('</itunes:owner>')
    if imageurl:
        base.append('<itunes:image href="{0}" />'.format(imageurl))
    if category:
        base.append('<itunes:category text="{0}">'.format(category))
        if subcategory:
            base.append('<itunes:category text="{0}"/>'.format(subcategory))
        base.append('</itunes:category>')
    base.append(items)
    base.append('</channel></rss>')
    return ''.join(base)

def createitem(title = '', author = '', subtitle = '', summary = '', imageurl = '',
               enclosureurl = '', enclosurelength = '', enclosuremime = '', guid = '',
               pubdate = '', duration = '', keywords = ''):
    #the things that aren't in if statements are the actual required fields.
    item = ['<item>']
    item.append('<title>{0}</title>'.format(title))
    if author:
        item.append('<itunes:author>{0}</itunes:author>'.format(author))
    if subtitle:
        item.append('<itunes:subtitle>{0}</itunes:subtitle>'.format(subtitle))
    if summary:
        item.append('<itunes:summary>{0}</itunes:summary>'.format(summary))
    if imageurl:
        item.append('<itunes:image href="{0}" />'.format(imageurl))
    item.append('<enclosure url="{0}" length="{1}" type="{2}" />'.format(enclosureurl, enclosurelength, enclosuremime))
    if guid:
        item.append('<guid>{0}</guid>'.format(guid))
    if pubdate:
        item.append('<pubDate>{0}</pubDate>'.format(pubdate))
    if duration:
        item.append('<itunes:duration>{0}</itunes:duration>'.format(duration))
    if keywords:
        item.append('<itunes:keywords>{0}</itunes:keywords>'.format(keywords))
    item.append('</item>')
    return ''.join(item)

def create_feed(files = [], title = 'My Podcast'):
    #example text taken from http://www.apple.com/itunes/podcasts/specs.html#example
    items = []
    for f in files:
        dirpath, basefile = os.path.split(f)
        basename, ext = os.path.splitext(basefile)
        try:
            filesize = os.stat(f)[6]
            if not ext in mime_mapping:
                print 'Warning: file type not supported!'
                return ''
            items.append(createitem(title = basename,
                                    enclosureurl = os.path.abspath(f),
                                    enclosurelength = filesize,
                                    enclosuremime = mime_mapping[ext]))
        except:
            items.append(createitem(title = basename,
                                    enclosureurl = f,
                                    enclosuremime = mime_mapping[ext]))
    items = ''.join(items)
    feed = createbase(title = title, items = items)
    return feed

def save(feed, fp):
    with open(fp, 'w') as f:
        f.write(feed)
        f.close()
        print 'Feed written to', fp

def main():
    parser = optparse.OptionParser(usage = '%prog [options] file1.. filen')

    parser.add_option('-t', help = 'Define a title',
                      action = 'store', type = 'string', dest = 'title')

    parser.add_option('-o', help = 'Define output file',
                      action = 'store', type = 'string', dest = 'filepath')

    options, args = parser.parse_args()

    if options.title is None:
        feed = create_feed(args)
    else:
        feed = create_feed(args, options.title)

    if not feed:
        print 'Warning: Could not generate feed!'
        return

    if options.filepath is None:
        fp = 'feed.xml'
    else:
        fp = options.filepath

    save(feed, fp)

if __name__ == '__main__':
    main()

