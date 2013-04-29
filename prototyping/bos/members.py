from util import lxmlize


MEMBER_LIST = "http://www.cityofboston.gov/citycouncil/"


def get_one(page, expr):
    ret = page.xpath(expr)
    if len(ret) != 1:
        print page.text_content()
        raise Exception("Bad xpath")
    return ret[0]


def scrape_page(href):
    page = lxmlize(href)
    ret = {}
    ret['bio'] = page.xpath(
        "//div[@class='content_main_sub']")[0].text_content().strip()

    ret['image'] = page.xpath(
        "//div[@class='sub_main_hd']//img")[0].attrib['src']

    return ret


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
        image = image.attrib['src']  # Fallback if we don't get one from the
        # homepage.
        homepage = name.attrib['href']
        name = name.text
        info = scrape_page(homepage)
        print info


if __name__ == "__main__":
    scrape_people()
