from util import lxmlize

CAL_PAGE = "http://www.santafenm.gov/currentevents.aspx"


def scrape_events():
    page = lxmlize(CAL_PAGE)
    for a in page.xpath("//a[contains(@href, 'CurrentEvents')]"):
        print a


if __name__ == "__main__":
    scrape_events()
