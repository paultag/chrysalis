from util import do_post_back, post_back, lxmlize
import re


PB_REG = re.compile(
    r"javascript:__doPostBack\('(?P<target>.*)','(?P<args>.*)'\)")


def scrape_bills():
    page = lxmlize("http://legistar.council.nyc.gov/Legislation.aspx")
    form = page.xpath("//form[@name='aspnetForm']")[0]

    page = post_back(form, **{
        "ctl00$ContentPlaceHolder1$btnSearch": "Search Legislation",
        "ctl00_tabTop_ClientState": '{"selectedIndexes":["1"],"logEntries":[],'
            '"scrollState":{}}',
        "ctl00$ContentPlaceHolder1$txtSearch": "",
    })

    for link in iterlinks(page):
        print link.text_content()


def iterlinks(page):
    next_page = None
    n = False
    for a in page.xpath("//td[@class='rgPagerCell NumericPages']//a"):
        if n:
            next_page = a
            break

        if a.attrib['class'] == 'rgCurrentPage':
            n = True

    for x in page.xpath("//a[contains(@href, 'LegislationDetail')]"):
        yield x

    if next_page is not None:
        info = PB_REG.match(next_page.attrib['href']).groupdict()
        form = page.xpath("//form[@name='aspnetForm']")
        form = form[0] if form else None
        if form is None:
            raise Exception("Form is None")

        npage = do_post_back(form, info['target'], info['args'])
        for x in iterlinks(npage):
            yield x


if __name__ == "__main__":
    scrape_bills()
