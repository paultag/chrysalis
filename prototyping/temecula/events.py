from util import lxmlize, do_post_back
import re


CAL_PAGE = ("http://www.cityoftemecula.org/Temecula/Visitors/Calendar.htm")


def cleanup(foo):
    foo = re.sub("\s+", " ", foo).strip()
    return foo


def scrape_events():
    page = lxmlize(CAL_PAGE)
    form = page.xpath("//form[@name='Form1']")
    form = form[0] if form else None
    if form is None:
        raise Exception("Erm, crud.")
    page = do_post_back(form, 'Listview1$ddlCategory', '', **{
        "Listview1:ddlCategory": "1"
    })
    for event in scrape_event_page(page):
        print event


def scrape_event_page(page):
    for entry in page.xpath(
            "//table[@id='Listview1_DataGrid1']//tr[@class='mainText']"):
        title = None
        ret = {}
        for block in entry.xpath(".//td[@class='mainText']"):
            entries = block.xpath("./*")
            if "table" in (x.tag for x in entries):
                continue
            info = [cleanup(x.text_content()) for x in entries]
            if title is None:
                title = info[1]
                continue
            key = info.pop(0)

            val = None
            if "Time: " in key:
                _, val = key.split("Time: ", 1)
                start, end = val.split(" - ", 1)
                val = {"start": start,
                       "end": end}
                key = "time"
            else:
                val = info.pop(0) if info else None

            ret[key] = val
            if info != []:
                raise Exception("Erm. odd scrape.")

        if title is None:
            continue

        ret['title'] = title
        yield ret


if __name__ == "__main__":
    scrape_events()
