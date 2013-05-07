from util import lxmlize
import datetime as dt



def scrape_events():
    page = lxmlize("http://phila.legistar.com/Calendar.aspx/")
    main = page.xpath("//table[@class='rgMasterTable']")[0]
    rows = main.xpath(".//tr")[1:]
    for row in rows:
        print ""
        (name, date, time, where, agenda, minutes) = row.xpath(".//td")

        name = name.text_content().strip()  # leaving an href on the table
        time = time.text_content().strip()
        location = where.text_content().strip()

        if "Deferred" in time:
            continue

        all_day = False
        if time == "":
            all_day = True
            when = dt.datetime.strptime(date.text.strip(),
                                        "%m/%d/%Y")
        else:
            when = dt.datetime.strptime("%s %s" % (date.text.strip(), time),
                                        "%m/%d/%Y %I:%M %p")

        agendas = agenda.xpath(".//a[@href]")
        for a in agendas:
            print a.text, a.attrib['href']

        minutes = minutes.xpath(".//a[@href]")
        for minute in minutes:
            print minute.text, minute.attrib['href']

        print name, when, location


if __name__ == "__main__":
    scrape_events()
