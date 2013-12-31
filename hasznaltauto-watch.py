#!/bin/python
#
# Watches a search URL on hasznaltauto.hu, and emails diffs between the two runs.
# Known issue: the search will time out after some time (days)
# Requirements: requests
#

from collections import namedtuple

search_url = 'http://www.hasznaltauto.hu/talalatilista/motor/SPAEYWPGG0GPFPWO31UGIYFQPYZEQMP1EHDF54Z0REELAK295OEOG23I4631C6C6EWJ3WL2HM0JGSOR58FLTHRR5RROUC49CFH4HU8AL5AHH5OW30C62T207OHCIL74L2KT4TC4D03ME374ED8PJO3C2A8JH9T5EH01QI0PWIHOC32DDTCQOY0123O3YQ671TLDKYICCQE94PA7JM83A8HHAH9DKEH4M7A28G4QMOJ9MPG329404CC3SF'
old_ads_filename = 'old-ads.bin'
Ad = namedtuple('Ad', ['title', 'url', 'thumb_url', 'price'])

def load_old_ads():
    import pickle
    old_ads = set()
    try:
        with open(old_ads_filename) as f:
            old_ads = pickle.load(f)
    except:
        pass
    return old_ads

def save_new_ads(new_ads):
    import pickle
    with open(old_ads_filename, 'w') as f:
        pickle.dump(new_ads, f)

def get_ads(page_text):
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(page_text)
    ads = []
    ad_elems = soup.findAll('div', 'talalati_lista')
    for ad_elem in ad_elems:
        title_elem = ad_elem.find('div', 'talalati_lista_title').find('a')
        thumb_elem = ad_elem.find('img', 'kepborder')
        price_elem = ad_elem.find('div', 'talalati_lista_vetelar')
        ads.append(Ad(title_elem.text, title_elem['href'], thumb_elem['src'], price_elem.text))
    return ads

def get_page(search_url, page_index):
    import requests
    response = requests.get(search_url + '/page' + str(page_index))
    if response.status_code == 404:
        raise Exception('Search 404-ed')
    if response.history:
        return None
    return response.text.encode(response.encoding)

def report(created, deleted):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    me = "noreply@example.com"
    you = "keccsx@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Hasznaltauto valtozasok"
    msg['From'] = me
    msg['To'] = you

    def ad_html(ad):
        return '''<a href="%s"><img src="%s" />%s -- %s</a>''' % (ad.url, ad.thumb_url, ad.title, ad.price)

    def ads_html(ads):
        return '<br />'.join([ad_html(ad) for ad in ads])

    html = """<html><body>
        <h1>Search URL</h1>
        <a href="%s">%s</a>
        <h1>Created</h1>%s
        <h1>Deleted</h1>%s
    </body></html>""" % (search_url, search_url, ads_html(created), ads_html(deleted))

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

def main():
    old_ads = load_old_ads()
    new_ads = set()
    page = 1
    while (True):
        page_text = get_page(search_url, page)
        if page_text is None:
            break
        new_ads = new_ads.union(get_ads(page_text))
        page += 1

    # if old_ads != set():
    created = new_ads.difference(old_ads)
    deleted = old_ads.difference(new_ads)
    report(created, deleted)

    save_new_ads(new_ads)

if __name__ == '__main__':
    main()
