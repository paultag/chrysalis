from util import lxmlize

MEMBER_PAGE = "http://council.nyc.gov/html/members/members.shtml"


def scrape_homepage(homepage):
    ret = {}

    page = lxmlize(homepage)

    ret['image'] = page.xpath(
        "//td[@class='inside_top_image']//img")[0].attrib['src']

    bio = page.xpath("//td[@class='inside_sub_feature']")[0]
    ret['bio'] = bio.text_content()

    #infobox = page.xpath("//td[@class='inside_top_text']")[0]
    #infobits = infobox.xpath(".//strong")
    #for entry in infobox:
    #    k, v = entry.text, entry.tail
    #    if k == "Committees":
    #        print v

    return ret


def scrape_people():
    page = lxmlize(MEMBER_PAGE)
    for entry in page.xpath("//table[@id='members_table']//tr"):
        entries = entry.xpath(".//td")
        if entries == []:
            continue

        name, district, borough, party = entries
        name = name.xpath(".//a")[0]
        homepage = name.attrib['href']
        name, district, borough, party = [x.text for x in
                                          [name, district, borough, party]]

        info = scrape_homepage(homepage)
        # person = Person(name, district=district, borough=borough,
        #                 party=party)
        print name, district, borough, party


if __name__ == "__main__":
    scrape_people()
