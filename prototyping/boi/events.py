from sh import pdftotext
import urllib2
import os
import re


CAL_PDF = ("http://www.cityofboise.org/city_clerk/HearingSchedule/"
           "HearingSchedule.pdf")

MONTHS = [
    "JANUARY",
    "FEBRUARY",
    "MARCH",
    "APRIL",
    "MAY",
    "JUNE",
    "JULY",
    "AUGUST",
    "SEPTEMBER",
    "OCTOBER",
    "NOVEMBER",
    "DECEMBER"
]

DATE_FINDER = re.compile(
    r"(?P<month>%s) (?P<day>\d{1,2}), (?P<year>\d{4})" % ("|".join(MONTHS))
)

TIME_FINDER = re.compile(r"\d{1,2}:\d{1,2} \w+")


def download_file(url):
    fpath = os.path.basename(url)
    if not os.path.exists(fpath):
        open(fpath, 'wb').write(urllib2.urlopen(url).read())
    return fpath


def scrape_events():
    path = download_file(CAL_PDF)
    target = re.sub("\.pdf$", ".txt", path)
    if not os.path.exists(target):
        pdftotext(path)

    entries = parse_file(open(target, 'r'))
    next(entries)  # two ignorable lines
    next(entries)

    for entry in entries:
        handle_buffer(entry)


def handle_buffer(buf):
    dates = DATE_FINDER.findall(buf)
    if dates == []:
        return
    month, day, year = dates[0]
    _, buf = buf.split(year, 1)
    time = TIME_FINDER.findall(buf)
    time = time[0] if time else None

    all_day = time is None
    print time, all_day


def parse_file(fd):
    collect = ""
    for line in fd.readlines():
        line = line.strip()
        if True in (x in line for x in MONTHS):
            yield collect
            collect = line
            continue
        collect += " " + line


if __name__ == "__main__":
    scrape_events()
