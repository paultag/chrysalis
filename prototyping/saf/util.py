import urllib2
import lxml.html


def lxmlize(url):
    entry = urllib2.urlopen(url)
    page = lxml.html.fromstring(entry.read())
    page.make_links_absolute(url)
    return page
