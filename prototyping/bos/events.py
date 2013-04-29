from util import lxmlize



def scrape_events():
    page = lxmlize(
        "http://www.cityofboston.gov/cityclerk/citycouncil/meetings.asp")
    print page

if __name__ == "__main__":
    scrape_events()
