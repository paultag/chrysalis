from util import lxmlize


MEMBER_LIST = "http://www.cityofboston.gov/citycouncil/"


def get_one(page, expr):
    ret = page.xpath(expr)
    if len(ret) != 1:
        print page.text_content()
        raise Exception("Bad xpath")
    return ret[0]


def scrape_page(href):
    pass


def scrape_people():
    page = lxmlize(MEMBER_LIST)
    people = page.xpath(
        "//table[@width='100%']//td[@style='TEXT-ALIGN: center']")

    for person in people:
        image, name = [get_one(person, x) for x in [
            ".//img",
            ".//a[contains(@href, 'councillors') and (text()!='')]"
        ]]
        role = person.xpath(".//br")[0].tail.strip()
        image = image.attrib['src']
        homepage = name.attrib['href']
        name = name.text
        print role, image, homepage, name



if __name__ == "__main__":
    scrape_people()
