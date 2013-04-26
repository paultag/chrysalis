from util import lxmlize
import re


INFOSLUG = re.compile(r"Ward (?P<district>\d+) Council(?P<gender>.*)")


def scrape_page(url):
    ret = {}
    page = lxmlize(url)
    bio = page.xpath("//div[@class='biotab bio']")[0].text_content()
    ret['bio'] = bio
    email = page.xpath(
        "//a[contains(@href, 'mailto:')]"
    )[0].attrib['href'].strip()[len("mailto:"):]
    ret['email'] = email
    committees = page.xpath("//ul[@class='list-flat']//li")
    ret['committees'] = [x.text for x in committees]
    contact = page.xpath("//div[@class='sidebar-content']//p")[0]

    contact_details = dict([y.strip().split(":", 1) for y in [contact.text]
                            + [x.tail for x in contact.xpath(".//br")] if y
                            and ":" in y])
    ret['contact_details'] = contact_details
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

        # Person(who,
        #        district=info['district'],
        #        gender=info['gender'],
        #        image=img,
        #        bio=contact-details.bio)
        #
        # person.add_committee_membership(what) for what in committees
        # yield person
        # Membership(person.id, self.org.id, role=role)
        #   --> Add contact_details
        #
        # yield membership


if __name__ == "__main__":
    scrape_people()
