import urllib
import urllib2
import lxml.html
import time


def lxmlize(url):
    time.sleep(4)
    entry = urllib2.urlopen(url)
    page = lxml.html.fromstring(entry.read())
    page.make_links_absolute(url)
    return page


def post_back(form, **kwargs):
    block = {name: value for name, value in [(obj.name, obj.value)
                for obj in form.xpath(".//input")]}
    block.update(kwargs)

    data = urllib.urlencode(block)
    ret = lxml.html.fromstring(urllib2.urlopen(form.action, data).read())

    ret.make_links_absolute(form.action)
    return ret


def do_post_back(form, event_target, event_argument):
    block = {}
    block['__EVENTTARGET'] = event_target
    block['__EVENTARGUMENT'] = event_argument
    return post_back(form, **block)
