import urllib2
import urllib

from util import lxmlize
import datetime as dt
import lxml
import re


CLICK_INFO = re.compile(r"CityCouncil\.popOverURL\('(?P<info_id>\d+)'\);")
ORD_INFO = re.compile(r"Ord\. No\. (?P<ord_no>\d+-\d+)")
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
        when = dt.datetime.strptime(popage.xpath("//strong")[0].text,
                                    "%B %d, %Y @ %I:%M %p")
        who = popage.xpath("//h1")[0].text
        related = []

        for item in popage.xpath("//div"):
            t = item.text
            if t is None:
                continue

            t = t.strip()
            for related_entity in ORD_INFO.findall(t):
                related.append({
                    "ord_no": related_entity,
                    "what": t
                })

        print who, when, related


if __name__ == "__main__":
    scrape_events()
