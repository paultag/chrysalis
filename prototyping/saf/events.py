from util import lxmlize
import datetime as dt
import re

CAL_PAGE = "http://www.santafenm.gov/currentevents.aspx"


def scrape_event(href):
    page = lxmlize(href.attrib['href'])
    tab = page.xpath("//table[@class='detail_content']")
    tab = tab[0] if tab else None
    if tab is None:
        return

    trs = tab.xpath("./tr")
    ret = {}
    for tr in trs:
        key, value = tr.xpath("./*")
        key = key.text.strip()
        value = re.sub(r"\s+", " ", value.text_content()).strip()
        ret[key] = value

    day = ret['Date:']
    fmt = "%B %d, %Y %I:%M %p"
    start, end = [dt.datetime.strptime("%s %s" % (day, x), fmt)
                  for x in [ret['Start Time:'], ret['End Time:']]]
    title = ret['Title:']
    descr = ret['Description:']
    location = ret['Address:']
    print start, title, end


def scrape_events():
    page = lxmlize(CAL_PAGE)
    for a in page.xpath("//a[contains(@href, 'CurrentEvents') "
                        "and (text()='More Information')]"):
        scrape_event(a)


if __name__ == "__main__":
    scrape_events()
