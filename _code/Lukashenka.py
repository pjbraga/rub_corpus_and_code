#!/usr/bin/env python3

"""Lukashenka.py: Scrapes transcripts of speechs,
                  interviews, and offical press
                  releases made by nominal 
                  Belarusian President Aleksandr
                  Lukashenka. """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

"""
Description
    This crawling and scraping
    code has been tailored for
    the http://president.gov.by/
    webiste. 

Requirements
    (1) number of the webpage to 
        start scraping (see the 
        page_number variable below) 
        links from;
    (2) webpage to stop scraping 
        (see the end_page_number varible
        below).

Summary of Code
    Its operation be understood 
    in three stages. First, it 
    goes to an archive webpage 
    on the president.gov.by 
    website and finds links
    to articles contianing 
    things said by Lukashenka. 
    These links are put into a 
    list. Second, each link 
    within the list is opened 
    and any relevant data is 
    scraped. Third, the text 
    within the data is processed
    and written to a storage
    file.

Notes
    Under each function, there is a 
    short description of its use. 
    In some cases, there are comments 
    explaining the purpose of
    certain variables, regular 
    expressions, or filters contained
    within functions.
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

# Storage/Output File
writeTOfile = codecs.open("PATH-TO-WHERE-YOU-" \
    "WANT-TO-SAVE-THE-SCRAPED-TEXTS", 'w+', \
    encoding='utf-8')

""" Note: 
    If and when the crawler/scraper
    is interrupted or freezes, 
    comment out the “Storage/Output File
    path above, and uncomment the file path
    directly below. Be sure that:
    (1) existing storage file must 
        be .csv file;
    (2) first line of .csv file must 
        contain the following: 
        date,href,speech
"""
# Append to storage/output file
# writeTOfile = codecs.open("PATH-TO-WHERE-YOU-" \
#    "WANT-TO-SAVE-THE-SCRAPED-TEXTS", 'a', \
#     encoding='utf-8')


def main():
    header()
    crawler_scraper()
    finish()


def header():
    """ creates .csv storage
        file. Writes dataset
        header row names.
        Only needs to be used
        when first starting the
        crawler/scraper. If it is
        not turned off after the 
        first use, it will overwrite
        the existing storage file.
    """
    print("Storage file created.")
    writer = csv.writer(writeTOfile)
    # Storage .csv header row names:
    writer.writerow(('date', 'address', 'speech'))

# Start of crawler functions (scroll down)
def address(page_number):
    """ Takes page number for archive
        webpage. Page number is what drives
        the while loop, which powers
        the crawler.
    """
    page = page_number
    html = "http://president.gov.by/ru/news_ru/archive/page/{}".format(page)
    try:
        webpages = urlopen(html) 
    except Exception as e:
        print ("Page number {} has an exception: {}").format(page, e)
        time.sleep(2)

    bsObj = BeautifulSoup(webpages, features="html.parser")
    
    return bsObj

def hrefCompile(bsObj):
    """ This function scrapes the
        hrefs to article, which in 
        turn need to be scraped.
        The hrefs are put into a
        list.
    """
    # href scraping method found here: 
    # https://stackoverflow.com/questions/48208905/google-scraping-href-values
    links = bsObj.select("div.bc_item_header a[href]")
    hrefs = []
    for link in links:
        hrefs.append(link['href'])
    
    prefix = "http://president.gov.by/ru/news_ru/printv"
    hrefsPrintv = []
    for href in hrefs:
        hrefsPrintv.append(prefix + href[39:])

    links = hrefsPrintv
    
    return links
# End of crawler functions.

# Start of text processing functions (scroll down)
def variables(bsObj, html):
    """ Used in scraper() below.
        After bsObj is created, 
        this function assigns 
        webpage html content 
        to variables, which 
        facilitate text processing.
    """
    print("Assigning html content to variables.")
    try:
        # date:
        date = bsObj.find("div", attrs={"class": \
            "pv_date"}) 
    except Exception as e:
        print("There is an exception for date variable:" \
            "{}.".format(e))
        time.sleep(2)
        pass

    try:
        # href:
        href = bsObj.select(".pv_ref a")
        for link in href:
            href = link["href"]
    except Exception as e:
        print("There is an exception for href" \
            " variable: {}.".format(e))
        time.sleep(2)
        pass

    try:
        # text:
        text = bsObj.find("div", attrs={"id": \
            "pv_main_part"})
    except Exception as e:
        print("There is an exception for text" \
            " variable: {}.".format(e))
        time.sleep(2)
        pass

    holder = pd.Series([date, href, text], \
        index=['date', 'href', 'text'])
    return holder

def textClean(holder):
    """ This function is used within
        the scraper() function (see below).
        It processes the text gathered in
        variables(), and prepares it to 
        be placed within a dataset.
    """
    date = holder['date']
    href = holder['href']
    text = holder['text']

    # Clean and arrange variables:
    # Date cleaner
    strDate = date.get_text()
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    cleaned_date = datetime.datetime.strptime(strDate, \
        u'%d %B %Y года').strftime('%Y-%m-%d')
    date = cleaned_date

    # Text processing prep
    """ This step converts bsObj into
        a string, which enables the
        data to be text processed. 
    """
    strText = str(text)

    # Filter for articles w/out quotation marks 
    """ Certain webpages, which bear
        the titles contained in the
        “filterSet” list, contain no
        quotation marks when Lukashenka
        speaks, but only feature
        Lukashenka speaking. Therefore, 
        the whole article can be scaped.
    """
    filterSet = ['<h1>Выступление', '<h1>НОВОГОДНЕЕ ОБРАЩЕНИЕ', \
        '<h1>Послание', '<h1>Поздравление', '<h1>Христианам', \
        '<h1>Заключительное', '<h1>Стенограмма', '<h1>Доклад', \
        '<h1>Приветствие', '<h1>Православным', 'СТЕНОГРАММА', \
        '<h1>Заявление', '<h1>Новогоднее', ]
    if any(word in strText for word in filterSet):
        detergent = re.compile(r'<.*?>')
        htmlScrubbed = re.sub(detergent, u'', strText)
        noNewLines = htmlScrubbed.replace(u'\n', u' ')
        noTabs = noNewLines.replace(u'\t', u'')
        noDoubleSpace = noTabs.replace(u'  ', u' ')

        time.sleep(1)
        print("Variables cleaned.")

        # Pack and pass data to next function
        lowerText = noDoubleSpace.lower()
        text = lowerText
        wrap = pd.Series([date, href, text], \
            index=['date', 'href', 'text'])
        return wrap
    
    # Filter for interview style artilces
    """ This is necessary for articles
        lacking quotation marks and 
        having multiple speakers.
    """
    filterSet = ['<h1>Интервью', '<h1>Участие', 'пресс-конференции']
    if any(word in strText for word in filterSet):
        noisy_text = re.findall(r'(?:(?<=Лукашенко А\.Г\.:<\/b>)|(?<=Лукашенко А\.Г\.:.<\/b>)|(?<=Лукашенко А\.Г\.<\/b>:)|(?<=Лукашенко)|(?<=Президент:)|(?<=<br \/>Ответ))[\s\S]*?(?=<div><b>|<\/div>\n<\/div>|Вопрос <br \/>|Вопрос<br \/>|<\/div>$|\.\.\.<br \/>|AFP|WSJ|Файнэшнл таймс|ФТ|Франфуртер Альгемайне Цайтунг|ФАЦ|газета|Новый век|Известия|Орловская правда|РИА|ТРК|ГТРК|телерадиокомпания)', strText)
        strInterview = str(noisy_text)
        detergent = re.compile(r'<.*?>')
        htmlScrubbed = re.sub(detergent, u'', strInterview)
        noise_rmv1 = re.sub(r'(\\xa0\\n\\n\\n\\n)|(\\xa0\\n\\n)|(\\xa0)|(\\n)', u' ', htmlScrubbed)
        noDoubleSpace = noise_rmv1.replace(u'  ', u' ')
        noise_rmv2 = noDoubleSpace.replace(u"']", u"")
        noise_rmv3 = noise_rmv2.replace(u"[' ", u"")
        noise_rmv4 = noise_rmv3.replace("', '", u"")

        time.sleep(1)
        print("Variables cleaned.")

        # Pack and pass data to next function
        lowerText = noise_rmv4.lower()
        text = lowerText
        wrap = pd.Series([date, href, text], \
            index=['date', 'href', 'text'])
        return wrap

    # Primary article cleaner
    """ Now that the filters above
        have caught all the articles
        with exceptions, articles in
        standard format can have 
        Lukashenka's speech extracted.
        This step removes special 
        characters for generic articles.
        The point is to make all the
        text the same before it is
        processed.
    """
    rightQuote = strText.replace(u'",', u'»,')
    rightQuoteStop = rightQuote.replace(u'". ', u'». ')
    rightQuoteTag = rightQuoteStop.replace(u'".<br', u'». <')
    leftQuote = rightQuoteTag.replace(u'"', u'«')
    detergent = re.compile(r'<.*?>')
    htmlScrubbed = re.sub(detergent, u'', leftQuote)
    noNewLines = htmlScrubbed.replace(u'\n', u' ')
    noTabs = noNewLines.replace(u'\t', u'')
    text = noTabs

    # Quotation extractor
    """ This step extracts anything
        that is said by anyone in a
        given article. It finds text
        within quotation marks, and
        highlights the text and speaker.
        Next, it scans the text samples
        with a series of expressions
        and pronouns (keywords), which 
        all refer to Lukashenaka. This
        way, only things said by 
        Lukashenka are extracted. The 
        quotations accompanied by these 
        keywords are appended to a list
        (see luka_list).
    """
    textLower = text.lower()
    pattern = r'([^\.]+«)(.*?)(».*?\.)'
    captureList = re.findall(pattern, textLower)

    keywords = ['президент республики беларусь', 'глава государства', \
        'александр лукашенко', 'президент беларуси', 'белорусский лидер', \
        'подчеркнул александр лукашенко', \
        'заключил президент', 'заявил президент', 'он также заявил', \
        'убежден президент', 'по словам президента', 'отметил президент', \
        'глава белорусского государства', 'сказал президент']

    luka_list = []
    for items in captureList:
        for sets in items:
            if any(word in sets for word in keywords):
                luka_list.append(items)
    
    # Cleaing Noise From Extractor
    """ Converts list of Lukashenka's 
        quotations to string, removes 
        tuple and list characters.
    """ 
    strQuotes = str(luka_list)
    noise_rmv1 = strQuotes.replace(u"', '", u"")
    noise_rmv2 = noise_rmv1.replace(u"'), ", u"")
    noise_rmv3 = noise_rmv2.replace(u"('", u"")
    noise_rmv4 = noise_rmv3.replace(u"[", u"")
    noise_rmv5 = noise_rmv4.replace(u"')]", u"")
    noise_rmv6 = re.sub(r'(\\xa0)|(    )',u' ' , noise_rmv5)
    noDoubleSpace = noise_rmv6.replace(u'  ', u' ')
    noEmptyCells = noDoubleSpace.replace(u']', u'пустая клетка')

    time.sleep(1)
    print("Variables cleaned.")

    # Pack and pass data to next function
    text = noEmptyCells
    wrap = pd.Series([date, href, text], \
        index=['date', 'href', 'text'])
    return wrap

def rowWriter(wrap):
    """ Writes collected data,
        date, href, and text, to
        a dataset.
    """
    date = wrap['date']
    href = wrap['href']
    text = wrap['text']

    writer = csv.writer(writeTOfile)
    writer.writerow((date, href, text))

    print("date: {}\nhref: {}\nwritten to file\n".format(date, href))
    time.sleep(1)
# End of data processing functions

# Scraper:
def scraper(links):
    """ Utilises href “links” collected 
        by the address() and 
        hrefCompile() functions. Below,
        the link (a URL) is opened online, 
        and its HTML contents are syntheised
        into a BeautifulSoup object (bsObj).
        Next, the variables() function gets 
        the date, href, and text for each
        article/speech. Next, textClean() 
        extracts the words said by 
        Lukashenka. Finally, rowWriter() 
        writes these words to a .csv dataset.
    """
    for link in links:

        # Opening Webpage
        html = link
        try:
            webpage = urlopen(html)
            time.sleep(2)
        except Exception as e:
            print("The test page has an exception:\n{}".format(e))
            time.sleep(2)
        
        # beautifulSoup Object Creation
        bsObj = BeautifulSoup(webpage, features="html.parser")

        # Data Processing
        rowWriter(textClean(variables(bsObj, html)))

# Crawler:
def crawler_scraper():
    """ This function begins with the appropriate 
        archive webpage number (page_number). 
        Each archive webpage contains 10 to 
        20 or so links to speeches (referred to 
        in these notes articles). The online 
        archive is organised chronologically, 
        therefore, the archive webpage number 
        corresponds to the date from which I
        need to start gathering articles from. 
        The page_number(), address(), and 
        hrefCompile() functions gather the 20
        links for the articles to be scraped.
        The scraper() takes these links, opens
        the articles connected to them, and 
        extracts words said by Lukashenka 
        from them. The scraper() function 
        also contains the rowWriter() function,
        which writes to the storage file 
        (writeTOfile). The crawler_scraper() 
        function stops when the while-loop 
        within reaches the end_page_number.
    """
    page_number = 379
    end_page_number = 191
    while page_number >= end_page_number:
        scraper(hrefCompile(address(page_number)))
        print("The crawler has catalogued " \
            "articles on page #{}.\n".format(str(page_number)))
        time.sleep(3)
        page_number -= 1
        if page_number == end_page_number:
            break

def finish():
    """ Closes .csv dataset 
        file.
    """
    writeTOfile.close()
    print("Crawling and scraping Finished.")

if __name__ == "__main__": main()



