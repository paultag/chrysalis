from util import do_post_back, post_back, lxmlize


def scrape_bills():
    page = lxmlize("http://legistar.council.nyc.gov/Legislation.aspx")
    form = page.xpath("//form[@name='aspnetForm']")[0]
    page = do_post_back(form, 'ctl00$ContentPlaceHolder1$btnSwitch', '', **{
        "ctl00$ContentPlaceHolder1$btnSwitch": ""
    })

    form = page.xpath("//form[@name='aspnetForm']")[0]
    page = post_back(form, **{
        "ctl00_ContentPlaceHolder1_lstMax_ClientState": '{"value":"1000000"}',
        "ctl00$ContentPlaceHolder1$txtText": "",
        "ctl00_ContentPlaceHolder1_txtFileCreated1_dateInput_ClientState":
            '{"logEntries":[],"value":"All","text":"All Years","enabled":'
            'true,"checkedIndices":[],"checkedItemsTextOverflows":false}'

    })
    print page.text_content()
    print page.xpath("//table[@class='rgMasterTable']")


if __name__ == "__main__":
    scrape_bills()
