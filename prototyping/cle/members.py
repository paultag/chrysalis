from util import lxmlize


def scrape_people():
    page = lxmlize("http://www.clevelandcitycouncil.org/council-members/")
    table = page.xpath("//div[@class='standard-content column']//table")[0]
    for person in table.xpath(".//td[@align='center']"):
        strong = person.xpath(".//strong")[0]
        who = strong.text.strip()
        role = strong.xpath("./br")[0].tail.strip()
        img = person.xpath(".//img")[0].attrib['src']
        print who, role, img


if __name__ == "__main__":
    scrape_people()
