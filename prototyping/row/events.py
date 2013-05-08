from util import lxmlize

CAL_PAGE = ("http://www.roswell-nm.gov/evlist/index.php?view=month&year=2013&"
            "month=5&day=0&cal=0&cat=0")


def scrape_event(event):
    page = lxmlize(event.attrib['href'])
    title = page.xpath("//h2[@class='evlist_header']")
    title = title[0].text.strip() if title else None
    if title is None:
        return
    if "CANCELED" in title:
        return

    info = page.xpath("//div[@style='position:relative;margin-right:40px;']")[0]
    blocks = info.xpath(".//div")
    ret = {}
    for block in blocks:
        els = block.xpath("./*")
        if not els:
            continue
        le = els[0]

        if le.tag != 'label':
            continue

        label, div = els

        ltex = label.text_content().strip()
        dtex = div.text_content().strip()
        ret[ltex] = dtex
    # do stuff with `ret'


def scrape_events():
    page = lxmlize(CAL_PAGE)
    days = page.xpath("//table[@class='evlist_month']//td")
    for day in days:
        when = day.xpath(".//span[@class='date_number']//a")
        when = when[0].text if when else None
        if when is None:
            continue
        events = day.xpath(".//a[contains(@href, 'event.php')]")
        for event in events:
            scrape_event(event)


if __name__ == "__main__":
    scrape_events()
