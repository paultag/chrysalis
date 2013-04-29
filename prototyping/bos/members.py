from collections import defaultdict
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
    main = get_one(page, "//div[@class='content_main_sub']")
    things = main.xpath("./*")
    cur = None

    split = {
        "chair": None,
        "email": None,
        "liaison": ",",
        "members": ",",
        "vice-chair": None,
        "description": None,
    }

    flags = {
        "Committee Chair:": "chair",
        "Committee E-mail:": "email",
        "Committee Members:": "members",
        "Committee Liaison:": "liaison",
        "Committee Liaison(s):": "liaison",
        "Committee Vice Chair": "vice-chair",
        "Committee Vice Chair:": "vice-chair",
        "Committee Description:": "description",
    }

    ret = defaultdict(list)
    for entry in things:
        if entry.tag == "h4":
            cur = flags[entry.text.strip()]
            continue

        e = entry.text_content()
        if e == "":
            continue

        if split[cur]:
            e = [x.strip() for x in e.split(split[cur])]
        else:
            e = [e]

        ret[cur] += e

    return ret


def scrape_committees():
    page = lxmlize(COMMITTEE_LIST)
    committees = page.xpath(
        "//a[contains(@href, 'committee') and contains(@href, 'asp')]")
    for c in committees:
        if c.text is None:
            continue
        name = c.text
        info = scrape_committee_page(c.attrib['href'])
        # committee = Committee(name)
        print name
        for member in info['members']:
            # committee.add_member(member, role='member')
            print member

        chair = info.get('chair', None)
        if chair:
            chair = chair[0]
            # committee.add_member(chair, role='chair')
            print "CHAIR:", chair

        vchair = info.get('vice-chair', None)
        if vchair:
            vchair = vchair[0]
            # committee.add_member(vchair, role='vice-chair')
            print "VICE-CHAIR:", vchair

        email = info.get('email', None)
        if email:
            email = email[0]
            # committee.add_contact_detail(email, 'committee email', 'email')
            print "EMAIL:", email
        # yield committee
        print ""

if __name__ == "__main__":
    scrape_people()
    scrape_committees()
