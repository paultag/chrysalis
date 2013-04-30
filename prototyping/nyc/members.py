from util import lxmlize
import urllib
import re


MEMBER_PAGE = "http://council.nyc.gov/html/members/members.shtml"
COMMITTEE_BASE = "http://council.nyc.gov/includes/scripts"
COMMITTEE_PAGE = "{COMMITTEE_BASE}/nav_nodes.js".format(**locals())
JS_PATTERN = re.compile(r"\s+\['(?P<name>.*)','(?P<url>.*)',\],")


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


def committees():
    page = urllib.urlopen(COMMITTEE_PAGE).read()
    active = False
    for line in page.splitlines():
        if "['Committees','" in line:
            active = True
            continue
        if active and not line.endswith("',],"):
            active = False
            continue

        if active:
            line = JS_PATTERN.match(line)
            if line is None:
                continue

            ret = line.groupdict()
            encoding_lame_bits = {
                "\\'": "'"
            }
            for k, v in encoding_lame_bits.items():
                ret['name'] = ret['name'].replace(k, v)

            ret['url'] = "%s/%s" % (COMMITTEE_BASE, ret['url'])
            yield ret


def scrape_committees():
    for committee in committees():
        print committee


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
    #scrape_people()
    scrape_committees()
