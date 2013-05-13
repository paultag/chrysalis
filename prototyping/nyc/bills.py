from util import do_post_back, post_back, lxmlize


def scrape_bills():
    page = lxmlize("http://legistar.council.nyc.gov/Legislation.aspx")
    form = page.xpath("//form[@name='aspnetForm']")[0]

    page = post_back(form, **{
        "ctl00$ContentPlaceHolder1$btnSearch": "Search Legislation",
        "ctl00_tabTop_ClientState": '{"selectedIndexes":["1"],"logEntries":[],'
            '"scrollState":{}}',

    })

    #print page.text_content()
    print page.xpath("//a[contains(@href, 'LegislationDetail')]")


if __name__ == "__main__":
    scrape_bills()
