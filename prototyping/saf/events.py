from util import lxmlize
import datetime as dt
import re

CAL_PAGE = "http://www.santafenm.gov/index.aspx?NID=1066"
DT = re.compile(r"(?P<time>\d{1,2}:\d{1,2}) (?P<ampm>AM|PM)")
WHEN = re.compile(r"DAY,\s+(?P<month>\w+)\s+(?P<dom>\d{1,2}),\s+(?P<year>\d{4})")


def cleanup(what):
    return re.sub("\s+", " ", what).strip()


def scrape_events():
    curdate = None
    page = lxmlize(CAL_PAGE)
    for el in page.xpath("//div[@id='Section1']/*"):
        if el.tag[0] == 'h':
            when = WHEN.findall(el.text_content())
            when = when[0] if when else None
            if when is None:
                continue
            curdate = " ".join(when)


        if el.tag == 'p' and el.attrib['class'] == 'MsoNormal':

            els = el.xpath("./*")
            agenda = el.xpath(".//a[contains(@href, 'Archive.aspx')]")
            agenda = agenda[0] if agenda else None
            if agenda is None:
                continue

            info = el.text_content()
            when = DT.findall(info)
            when = when[0] if when else None
            if when is None:
                continue

            people = el.xpath(".//personname")
            places = el.xpath(".//place")
            time, ampm = when

            tbuf = " ".join([curdate, time, ampm])
            obj = dt.datetime.strptime(tbuf, "%B %m %Y %I:%M %p")
            print obj


if __name__ == "__main__":
    scrape_events()
