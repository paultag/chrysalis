from util import lxmlize
import urllib2
import urllib
import lxml
import time


DURL = "http://www.cityofboston.gov/cityclerk/rollcall/default.aspx"


def do_post_back(form, event_target, event_argument):
    block = {name: value for name, value in [(obj.name, obj.value)
                for obj in form.xpath(".//input")]}
    block['__EVENTTARGET'] = event_target
    block['__EVENTARGUMENT'] = event_argument
    block['ctl00$MainContent$lblCurrentText'] = (
        int(block['ctl00$MainContent$lblCurrentText']) + 1)

    data = urllib.urlencode(block)
    ret = lxml.html.fromstring(urllib2.urlopen(form.action, data).read())

    ret.make_links_absolute(form.action)
    return ret


def iterpages():
    page = lxmlize(DURL)
    yield page
    while page:
        yield page
        page = next_page(page)


def next_page(page):
    time.sleep(4)
    form = page.xpath("//form[@name='aspnetForm']")[0]
    n = page.xpath("//a[contains(text(), 'Next Page')]")[0]
    nextable = n.attrib['style'] != 'display: none;'
    if nextable:
        return do_post_back(form, 'ctl00$MainContent$lnkNext', '')
    return None


for page in iterpages():
    for subject in page.xpath('//div[@class="ContainerPanel"]'):
        dates = subject.xpath(".//font[@color='#276598']/b/text()")
        motions = [x.strip() for x in subject.xpath(
            ".//div[@style='width:260px; float:left;']/text()")]
        votes = subject.xpath(".//div[@style='width:150px; float:right;']")

        for date, motion, vote in zip(dates, motions, votes):
            vit = iter(vote.xpath("./div"))
            vote = zip(vit, vit, vit)
            for who, entry, _ in vote:
                print who.text, entry.text

            print date, motion
