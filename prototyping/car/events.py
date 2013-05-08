from util import lxmlize

CAL_URL = ("http://www.townofcary.org/Town_Council/Meetings____"
           "Public_Notices_Calendar.htm")


def scrape_event(href):
    page = lxmlize(href.attrib['href'])
    what = page.xpath("//td[@id='ctl14_ctl16_tdTitleCell']")[0].text
    info = page.xpath("//div[@id='ctl14_pnlEvent']//table//table//tr")[1:]
    ret = {
        "Location:": "Unknown"
    }
    for tr in info:
        tds = tr.xpath(".//td")
        if len(tds) < 2:
            continue
        what, data = [tds.pop(0).text_content().strip() for x in range(2)]
        ret[what] = data

    agendas = page.xpath("//a[contains(@title, 'Meeting Agenda')]")
    if agendas:
        for agenda in agendas:
            print "Agenda:", agenda.attrib['href']
    print ret


def scrape_events():
    page = lxmlize(CAL_URL)
    events = page.xpath("//div[@id='ctl14_pnlCalendarAll']//td")
    for event in events:
        when = event.xpath(".//a[contains(@href, 'javascript')]")
        if when == []:
            continue
        when = when[0]

        dom = when.text  # day of month
        hrefs = event.xpath(".//a[contains(@href, 'htm')]")
        for href in hrefs:
            scrape_event(href)


if __name__ == "__main__":
    scrape_events()
