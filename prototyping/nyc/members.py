from util import lxmlize

MEMBER_PAGE = "http://council.nyc.gov/html/members/members.shtml"

def scrape_people():
    page = lxmlize(MEMBER_PAGE)
    print page


if __name__ == "__main__":
    scrape_people()
