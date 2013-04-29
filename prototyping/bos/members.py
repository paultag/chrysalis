from util import lxmlize


MEMBER_LIST = "http://www.cityofboston.gov/citycouncil/"
COMMITTEE_LIST = "http://www.cityofboston.gov/citycouncil/committees/"


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
        if info.get('image', None):
            image = info['image']

        # p = Legislator(name,
        #                district=role,
        #                image=image,
        #                bio=info['bio']
        #                homepage=homepage)
        # [implicit membership to council]
        # yield p
        print name, homepage


def scrape_committee_page(href):
    page = lxmlize(href)


def scrape_committees():
    page = lxmlize(COMMITTEE_LIST)
    committees = page.xpath("//a[contains(@href, 'committee')]")
    for c in committees:
        if c.text is None:
            continue
        scrape_committee_page(c.attrib['href'])

if __name__ == "__main__":
    # scrape_people()
    scrape_committees()
