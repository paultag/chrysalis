from util import lxmlize
import datetime as dt



def scrape_events():
    page = lxmlize(
        "http://meetingrecords.cityofboston.gov/sirepub/meetresults.aspx")
    for entry in page.xpath(
            "//tr[@style='font-family: Verdana; font-size: 12px;']"):
        name, when, links = entry.xpath(".//td")
        name = name.text.encode('latin-1').strip().replace("\xc2\xa0", "")
        when = when.text.encode('latin-1').strip().replace("\xc2\xa0", "")
        # XXX: Fix encoding; scrapelib ought to fix; strip sucks.
        when = dt.datetime.strptime(when, "%m/%d/%Y")
        links = links.xpath(".//a")
        links = {x.text: x.attrib['href'] for x in links}
        for k, v in links.items():
            print k, v


if __name__ == "__main__":
    scrape_events()
