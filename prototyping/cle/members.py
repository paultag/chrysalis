from util import lxmlize
import re


INFOSLUG = re.compile(r"Ward (?P<district>\d+) Council(?P<gender>.*)")


def scrape_page(url):
    ret = {}
    page = lxmlize(url)
    bio = page.xpath("//div[@class='biotab bio']")[0].text_content()
    ret['bio'] = bio
    # grab contact info
    # grab committees
    email = page.xpath(
        "//a[contains(@href, 'mailto:')]"
    )[0].attrib['href'].strip()[len("mailto:"):]
    ret['email'] = email
    return ret


def scrape_people():
    page = lxmlize("http://www.clevelandcitycouncil.org/council-members/")
    table = page.xpath("//div[@class='standard-content column']//table")[0]
    for person in table.xpath(".//td[@align='center']"):
        strong = person.xpath(".//strong")[0]
        who = strong.text.strip()
        role = strong.xpath("./br")[0].tail.strip()
        img = person.xpath(".//img")[0].attrib['src']
        info = INFOSLUG.match(role).groupdict()

        scraped_info = {}
        page = person.xpath(".//a")
        if page != []:
            page = page[0].attrib['href']
            scraped_info = scrape_page(page)

        print who, role, img, info

        # Person(who,
        #        district=info['district'],
        #        gender=info['gender'].
        #        image=img)
        #
        # yield person
        # Membership(person.id, self.org.id, role=role)
        # yield membership


if __name__ == "__main__":
    scrape_people()
