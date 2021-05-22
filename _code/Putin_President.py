#!/usr/bin/env python3

""" Putin_President.py: Scrapes transcripts of speechs,
                        interviews, and offical press
                        releases made by Vladimir Putin
                        when he served as Russian 
                        President """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

""" 
Description
    This code crawls links
    and scrapes speechs made
    by Russian President 
    Vladimir Putin from 2006 to
    2016. It is tailored for
    the website http://kremlin.ru.

Requirements
    (1) the webpage number (see variable
        “i” below) for the first speech
        needed;
    (2) the webpage number for the last
        speech (see variable “end_page_number”
        below) needed.

Summary of Code
    This code consists of three loops:
    (1) a “try/finally” loop; (2) a
    “while” loop; and (3) another “while”
    loop. 
    The “try/finally” loop is essentially 
    useless. It merely houses the two 
    other “while” loops that do all the 
    work.
    The first “while” loop is an iterator 
    driven by start and finish webpage 
    numbers (see variables “i” and
    “end_page_number” below). This loop
    contains all the crawling and scraping
    code.
    The second “while” loop is a date 
    filter, which divides the code in the 
    first while loop into its crawling 
    and scraping operations. Above 
    the filter, the code inputs webpage 
    links for speeches. This link is fed to 
    the filter, which checks if the speech
    attached to it was given on the right date.
    If the speech is the wrong date, the next
    link is fed to the filter, and 
    the crawling continues. If the speech 
    is given on a desired date, the code 
    moves on to scraping and text processing.
    Once a speech is scraped, the first 
    “while” loop increments.

Notes
    This was the first crawler-
    scraper code that the author
    wrote. Its composition was 
    a learning process. The code
    is rudimentary and often 
    inefficient. Allthesame, 
    it does the job.
"""

import csv
import codecs
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

"""
Some Notes on Parsing Putin's Speeches
as Russian President at Kremlin.ru
-----------------------------------------------------
Putin's first speech as returning 
president lists on kremlin.ru as 7 May 2012: 
http://kremlin.ru/events/president/transcripts/15224.

The index numnber for this first speech, “15224,” 
is at the end of the URL. 

The last speech Putin gives in 2016 has the 
index number of 53684. 

Therefore, this Crawler/Scraper must start (see 
variable “i” below) on 15224 and increment until
(see variable “end_page_number”) 53684.

On another note, the speeches do not appear
in chronological order.
-----------------------------------------------------
"""

def main():
    multi_speech_csv()

def multi_speech_csv():
    """ Uses a “while” 
        loop to write files 
        with another “while” loop 
        within it to cylce 
        through webpages until
        a speech from the correct
        date is found. Once a
        the date requirement is
        statisfied, the speech
        and other data, such 
        as the date and link
        to the article, are 
        scraped and written to
        a spreadsheet. Once
        a speech and other
        relevant data is scraped 
        and saved to the storage
        file, the “i” variable 
        (see below) increments. 
        The “try/finally” loop 
        runs until the “i” variable
        equals the “end_page_number”
        variable (also see below).
    """

    print("Scraping started.")
    csv_file = codecs.open("PATH-TO-WHERE-YOU-" \
    "WANT-TO-SAVE-THE-SCRAPED-TEXTS", \
            'w+', encoding='utf-8')

    # Crawler        
    try:
        end_page_number = 53684 # For the year 2016, the last page 53684.
        writer = csv.writer(csv_file)
        writer.writerow(('No.', 'Speaker', 'Date', 'Location', 'URL', 'Subject', 'Title', 'Description', 'Speech'))
        i = 15224 # For the year 2006, starting page number is 15224.
        num = 1 

        while i <= end_page_number:
            html = "http://kremlin.ru/events/president/transcripts/{}".format(i)
            try:
                pages = urlopen(html) 
            except Exception as e:
                print (e)
                time.sleep(2)
                i += 1      # This is here if the page does not exist, the page number changes, and the loop continues.
                continue
             
            bsObj = BeautifulSoup(pages, features="html.parser") # This is a date filter step.

            # This is a date filter. 
            # It is a while loop, which 
            # stays engaged until a date 
            # of 2006+ is found. 
            # Once the date criterion is 
            # satisfied, the while loop 
            # breaks and the code continues.
            dateFilter = bsObj.time.attrs['datetime']
            while float(dateFilter[:-6]) < 2006:
                print("Speech was given before 2006.")
                i += 1
                time.sleep(2)
                try: 
                    whileHTML = "http://kremlin.ru/events/president/transcripts/{}".format(i)
                    pages = urlopen(whileHTML)
                except Exception as e:
                    print (e)
                    i += 1
                    continue
                breakObj = BeautifulSoup(pages, features="html.parser")
                breakFilter = breakObj.time.attrs['datetime']
                if float(breakFilter[:-6]) >= 2006:
                    print("Date filter passed. Reassigning parsing variables.")
                    html = "http://kremlin.ru/events/president/transcripts/{}".format(i)
                    pages = urlopen(html) 
                    bsObj = BeautifulSoup(pages, features="html.parser")
                    break
                    
            # scraper
            # Who gave the speech:
            try:
                speaker = bsObj.find("a", attrs={"href":"http://putin.kremlin.ru/"})
            except Exception as e:
                print("There is an exception for speaker variable: {}.".format(e))
                continue

            # When was speech given:
            try:    
                timeOfPub = bsObj.time.attrs['datetime']
            except Exception as e:
                print("There is an exception for timeOfPub variable: {}.".format(e))
                time.sleep(2)
                continue

            # Where was speech given:
            try:
                place = bsObj.find("div", attrs={"class":"read__place p-location"})
                if place is None:
                    print("The place variable has a “None” value.\nReassigning place to “topline__in” Tag...")
                    time.sleep(2)
                    place = bsObj.find("div", attrs={"class":"topline__in"}).find("a")
                else: 
                    pass
            except Exception as e:
                print("There is an exception for place variable: {}.".format(e))
                time.sleep(2)
                print("Reassigning place to “topline__in” Tag...")
                place = bsObj.find("div", attrs={"class":"topline__in"}).find("a") 
                pass

            # What is the theme of the speech:
            try:
                subject = bsObj.find("li", attrs={"class":"p-category"}).find("a")
            except Exception as e:
                print("There is an exception for subject variable: {}.".format(e))
                time.sleep(2)
                print("Reassigning subject to “topline__in” Tag...")
                subject = bsObj.find("div", attrs={"class":"topline__in"}).find("a") # This is a “trick” piece of code to give my variable reassignments below something to work with.
                pass

            # What is the title of the speech
            try:
                title = bsObj.title 
            except Exception as e:
                print("There is an exception for title variable: {}.".format(e))
                time.sleep(2)
                continue

            # A short description of the speech:
            try:
                description = bsObj.find("head").findAll("meta", {"name":"description"})
            except Exception as e:
                print("There is an exception for description variable: {}".format(e))
                time.sleep(2)
                continue
            finally:
                print("Variable assignment complete.")

            # Text processing

            # After the below variable
            # assignments, the commented 
            # notes from 1 to 5 indicate
            # the various text processing
            # steps taken. 
            n = num
            a = speaker.get_text()[:-14]
            b = timeOfPub
            c = place.get_text()
            URL = html
            d = subject.get_text()
            e = title.get_text()[:-18]
            f = str(description)[16:-24]

            # The following variable assignments:
            # (1) gathers the div tag 
            # where speech is wrapped 
            # into a multiline string;
            speech_container = bsObj.find("div", attrs={"class":"entry-content e-content read__internal_content"}).findAll("p")
            # (2) converts bsObj from BeautifulSoup 
            # object into string that re can use;
            string_text = str(speech_container)
            # (3) filters unwanted 
            # data from the string;
            if re.findall(r'<b>В.Путин', string_text):  # This if/else loop is to deal with older speeches. 
                                                        # If it is during Putin's Second term, then his name is not in bold <b></b>, 
                                                        # therefore, my original Regex does not work. So, I need these two different Regexes.
                                                        # The first Regex is for older speeches (pre-2014). The second is for newer (post-2014).
                                                        # At times, the first Regex (for older speeches), will include the name of another 
                                                        # person Putin is speaking with. This “noise” in the text is acceptable, because
                                                        # names will not have an effect on the Sentiment Analysis later.
                noisy_text = re.findall(r'(?:(?<=Путин<\/b>)|(?<=Путин..<\/b>)|(?<=Путин.<\/b>))[\s\S]*?(?=<b|<div class="read_|Опубликован в)', string_text)
            else: 
                noisy_text = re.findall(r'(?:(?<=В.Путин:)|(?<=<p>))[\s\S]*?(?=:|<div class="read_|Опубликован в)', string_text)
            # (4) removes unwanted characters and leftover HTML from stirng;
            xa0_cleaner = [i.replace(u'\xa0', u' ') for i in noisy_text]
            p_end_tag_cleaner = [i.replace(u'</p>', u'') for i in xa0_cleaner]
            newLine_cleaner = [i.replace(u'\n', u' ') for i in p_end_tag_cleaner]
            p_start_tag_cleaner = [i.replace(u'<p>', u'') for i in newLine_cleaner]
            random_speechMark_cleaner = [i.replace(u"'", u"") for i in p_start_tag_cleaner]
            random_comma_remover = [i.replace(u' ,', u'') for i in random_speechMark_cleaner]
            punctuation_cleaner_1 = [i.replace(u'.,', u'.') for i in random_comma_remover]
            punctuation_cleaner_2 = [i.replace(u'!,', u'!') for i in punctuation_cleaner_1]
            ltgt_cleaner = [i.replace(u'&lt;…&gt;', u'') for i in punctuation_cleaner_2] #This removes a combination of <[someCharacterThatIDon'tKnow]>. 
            # (5) scrubs any random HTML that may still slip in;
            detergent = re.compile(r'<.*?>')    
            # It may seem repetitive (I remove HTML in the replacements above),
            # but after testing, this format yields the cleanest text.  
            washedHTML = [re.sub(detergent, u'', a) for a in ltgt_cleaner]
            g = str(washedHTML)

            # Writes to file at the top of the while loop:
            writer.writerow((n, a, b, c, URL, d, e, f, g))

            time.sleep(2)
            print("Scraper has catalogued {}".format(html))
            i += 1
            num += 1
            if i == end_page_number:
                break
    finally:
        csv_file.close()
        print("Scraping Finished.")

if __name__ == "__main__": main()