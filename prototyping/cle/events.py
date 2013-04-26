import urllib2
import urllib

from util import lxmlize
import lxml
import re


# 9:30 AM Health and Human Services Committee
EVENT_INFO = re.compile(r"(?P<when>\d+:\d+ (AM|PM)) (?P<ctty>.*) Committee")
CLICK_INFO = re.compile(r"CityCouncil\.popOverURL\('(?P<info_id>\d+)'\);")

AJAX_ENDPOINT = "http://www.clevelandcitycouncil.org/plugins/NewsToolv7/public/calendarPopup.ashx"


def popOverUrl(poid):
    data = {
        "action": "getCalendarPopup",
        "newsid": poid
    }
    page = urllib2.urlopen(AJAX_ENDPOINT, urllib.urlencode(data))
    page = lxml.html.fromstring(page.read())
    page.make_links_absolute(AJAX_ENDPOINT)
    return page


def scrape_events():
    page = lxmlize("http://www.clevelandcitycouncil.org/calendar/")
    events = page.xpath("//ul[contains(@class, 'committee-events')]//li")
    for event in events:
        string = event.text_content()

        po = CLICK_INFO.match(event.xpath(".//span")[0].attrib['onclick'])
        if po is None:
            continue

        poid = po.groupdict()['info_id']  # This is used to get more deetz on

        popage = popOverUrl(poid)
        print popage.text_content()

        e = EVENT_INFO.match(string)
        if e is None:
            continue
        e = e.groupdict()


if __name__ == "__main__":
    scrape_events()
