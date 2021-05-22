#!/usr/bin/evn python3

""" Putin_PM.py: Scrapes transcripts of speechs,
                 interviews, and offical press
                 releases made by Vladimir Putin
                 when he served as Russian 
                 Prime Minister """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"


""" 
Description
    Crawls URLs and
    scrapes speeches given 
    by Russian Prime Minister 
    Vladimir Putin from 
    2008–2012. This code is
    tailored for articles from
    the website:
    http://archive.premier.gov.ru/.

Requirements
    (1) webpage number for page to
        start scraping (see “Notes” in
        this comment block below);
    (2) webpage number for page to 
        stop scraping (See “Notes” in 
        this comment block below).

Summary of Code
    This code consists of three 
    functions to crawl and 
    scrape speeches from webpages.
    The first function, headerWriter(),
    creates a .csv storage file.
    The second function, crawlerScraper(),
    crawls URLs and scrapes the speeches.
    The different operations of this crawler/
    scraper are identified below by 
    comment hashes “#”. The whole function
    is a single “while” loop. 
    The last funciton, finish(), closes 
    the storage file.

Notes
    Putin's first speech as PM:
    http://archive.premier.gov.ru/events/news/1361/
    Putin's last speech as PM: 
    http://archive.premier.gov.ru/events/news/18909/

    Scraper start and stop:
         start page # is: 1361.
         stop page # is: 18909.
"""

import csv
import codecs
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import datetime
import locale
import re

# Give file name for output:
writeTOfile = codecs.open("PATH-TO-WHERE-YOU-" \
    "WANT-TO-SAVE-THE-SCRAPED-TEXTS", 'w+', encoding='utf-8')

def main():
    headerWriter()
    crawlerScraper()
    finish()

def headerWriter():
    """ Creates .csv storage 
        file for scraped 
        data to be written to.
    """

    print("Storage file created.")
    writer = csv.writer(writeTOfile)
    # Name of header rows:
    writer.writerow(('date', 'href', 'speech'))

def crawlerScraper():
    """ A while loop iterator
        that crawls URLs and 
        scrapes speeches made
        by Russian Prime 
        Minister Vladimir Putin
        from 2008 to 2012.
    """

    # Crawler
    page = 1361
    while page <= 18909:
        try:
            html = "http://archive.premier.gov.ru/" \
                "events/news/{}/".format(page)
            webpage = urlopen(html)
            time.sleep(2)
        except Exception as e:
            print ("Page number {} has an exception: {}".format(page, e))
            time.sleep(2)
            page += 1
            continue

        # Scraper

        # BeautifulSoup Object Created:
        bsObj = BeautifulSoup(webpage, features="html.parser")

        print("Assigning html content to variables.")
        # date of speech:
        try:
            date = bsObj.find("div", attrs={"class":"date"}).find("span")
        except Exception as e:
            print("There is an exception for date variable: {}.".format(e))
            time.sleep(2)
            pass
        
        # Speech:
        try:
            speech = bsObj.find("div", attrs={"id":"recordBox"})
        except Exception as e:
            print("There is an exception for timeOfPub" \
                " variable: {}.".format(e))
            time.sleep(2)
            pass

        # Text processing

        # Date formater:
        strDate = date.get_text()
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        cleaned_date = datetime.datetime.strptime(strDate, u'%d %B, %Y').strftime('%Y-%m-%d')
        date = cleaned_date

        # href:
        href = html

        # Putin Speech Filter:
        strSpeech = str(speech)
        noisy_text = re.findall(r'(?:(?<=Путин<\/strong>)|(?<=Путин.<\/strong>)|(?<=Путина.<\/strong>)|(?<=г.<\/strong>)|(?<=г..<\/strong>)|(?<=на заседании Правительства РФ:<\/strong>)|(?<=года:<\/strong>)|(?<=<strong>Вступительн))[\s\S]*?(?=<strong>|<\/div>)', strSpeech)

        # Speech text cleaner:
        detergent = re.compile(r'<.*?>')
        htmlScrubbed = [re.sub(detergent, u'', a) for a in noisy_text]
        nScrubbed = [i.replace(u'\n', u' ') for i in htmlScrubbed]
        r_Scrubbed = [i.replace(u'\r ', u'') for i in nScrubbed]
        _rScrubbed = [i.replace(u' \r', u'') for i in r_Scrubbed]
        speech = _rScrubbed

        time.sleep(1)
        print("Variables cleaned.")

        # Write to storage file
        writer = csv.writer(writeTOfile)
        writer.writerow((date, href, speech))
        time.sleep(1)
        print("Scraper has catalogued: {}.".format(href))

        # Iterate:
        page += 1

        if page == 18909:
            break

def finish():
    """ Closes storage file
        so no new data can be
        added.
    """
    writeTOfile.close()
    print("Scraping Finished.")

if __name__ == "__main__": main()