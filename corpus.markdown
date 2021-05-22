---
layout: page
title: RUB Corpus
cover: /rub_corpus_and_code/images/blue.png
permalink: /rub_corpus_and_code/corpus/
---
The RUB Corpus is a collection of Russian-language official government speeches, interviews, and press releases made by top policymakers in Russia, Ukraine, and Belarus from 2006 to 2016.

The Corpus is availabe for download under the “Corpus Download” heading below.

The Corpus is divided by country in plain text .tsv (tab-separated values) files.

### Introduction
The corpus is a collection of 71,515 Russian-language texts published
between 01 January 2006 to 31 December 2016. 

A text is sentences spoken by an incumbent president, prime minister, or minister of foreign affairs from a single speech, interview, or official press release on a particular date.

The sources for these texts are online, official government archives.

The texts were gathered as part of a PhD dissertation to trace how policymakers’ opinions on particular subjects changed over time.

Tracking what top policymakers say relates to the strong influence leaders and key officials have on policy development in nondemocratic regimes ([Ambrosio, 2017, pp. 203–204](https://doi.org/10.1080/21599165.2017.1304382); [Pavlovsky, 2016, pp. 10–16](https://www.foreignaffairs.com/articles/russia-fsu/2016-04-18/russian-politics-under-putin); [Rudyj, 2020, p. 198](https://oz.by/books/more10931323.html)).

The corpus can be used, for example, to analyse the sentiments (positive, negative, neutral, or ambiguous) of Russian-speaking, top policymakers on issues such as NATO, [democracy](/rub_corpus_and_code/visuals/), [bilateral relations](/rub_corpus_and_code/visuals/), and so on. 

The code used to carry out this sentiment analysis can be found on the [Code page](/rub_corpus_and_code/code/).

For examples of how the corpus and code can be used, see the [Data Visualisations page](/rub_corpus_and_code/visuals/).

### The Collections
The texts were gathered using Python 3.7.1 ([Van Rossum & Drake, 2018](https://www.python.org/downloads/release/python-371/)), BeautifulSoup 4.7.1 ([Richardson, 2019](https://www.crummy.com/software/BeautifulSoup/bs4/download/4.7/)) and other Python third party software (such as Pandas) to crawl webpages and scrape the relevant texts ([PyData Development Team, 2019](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.24.1.html); [Reitz, 2019](https://github.com/psf/requests-html)).

#### Russia
14,165 texts were collected for Vladimir Putin, Dmitry Medvedev, and Sergei Lavrov. Sources for Russian policymakers include the President of Russia website ([Kremlin, 2020](http://kremlin.ru/events/president/transcripts)), two Government of Russia websites for prime ministerial texts ([Government of Russia, 2020](http://government.ru/news/); [Office of the Prime Minister, 2012](http://archive.premier.gov.ru/events/news/)), and the Russian Ministry of Foreign Affairs website ([MFA of Russia, 2020](https://www.mid.ru/ru/press_service/minister_speeches/)).

#### Ukraine
51,827 texts were collected for 12 policymakers (four presidents and eight prime ministers). The sources for Ukraine’s policymakers are various iterations of its “Government Portal” ([Government Portal, 2017](http://old.kmu.gov.ua/kmu/control/publish/)), which archived the majority of top officials’ speeches and interviews from the early 2000s to the present. But when Ukrainian President Petro Poroshenko lost re-election to Zelenski in 2018, the portal’s presidential archive was abruptly taken offline. Therefore, the internet-archiving site, Wayback Machine ([Internet Archive, 2020](https://archive.org/help/wayback_api.php)), had to be used to source Ukrainian presidential texts. The still accessible elements of the Government Portal archive were used for the prime ministerial texts.

#### Belarus
5,523 texts were compiled for nominal Belarusian President Aleksandr Lukashenka only. Online resources for other top Belarusian policymakers were scattered, limited, or non-existent. Sources for Lukashenka, on the other hand, are comprehensive and compiled at the “President of Belarus” website ([Presidential Press Service of the Republic of Belarus, 2020](http://president.gov.by/ru/news_ru/archive/page/)).

### Corpus Download
To use any of the corpus collections, please use the following citation:

<p class=reference><strong>Braga, P.</strong> (2020). RUB Corpus and Code. Project repository. Available at:<a href="https://github.com/pjbraga/rub_corpus_and_code"> https://github.com/pjbraga/rub_corpus_and_code</a>.</p>

The RUB Corpus collections are currently available as zip files in .tsv format:

| ![Russia](/images/database_image.png) | ![Ukraine](/images/database_image.png) | ![Belarus](/images/database_image.png) |
| <a href="https://github.com/pjbraga/rub_corpus_and_code/raw/main/_corpus/russia_all_texts.tsv.zip">Russia</a> | <a href="https://github.com/pjbraga/rub_corpus_and_code/raw/main/_corpus/ukraine_all_texts.tsv.zip">Ukraine</a> | <a href="https://github.com/pjbraga/rub_corpus_and_code/raw/main/_corpus/belarus_all_texts.tsv.zip">Belarus</a> |
| Russian policymakers (Presidents/Prime Ministers Vladimir Putin and Dmitry Medvedev, and Minister of Foreign Affairs Sergei Lavrov) collection, 2006–2016 | Ukrainian policymakers (Presidents Viktor Yushchenko, Viktor Yanukovych, Oleksandr Turchynov, and Petro Poroshenko. Prime Ministers Yuri Yekhanurov, Viktor Yanukovych, Yulia Tymoshenko, Oleksandr Yurchynov, Mykola Azarov, Sergei Arbuzov, Arseniy Yatsenyuk, and Volodymyr Groysman) collection, 2006–2016 |  Belarusian policymaker (President Aleksander Lukashenka) collection, 2006–2016 |

### Corpus Organisation
Corpus texts are arranged in .tsv files. 

The first column gives a text's publication date, the second column has corresponding href for the text, and the third column contains the text. 

For example:
![Corpus Organisation](/rub_corpus_and_code/images/corpus_org.png)

### Questions or Issues
For issues with the RUB Corpus and Code repositories, please use <a href="https://github.com/pjbraga/rub_corpus_and_code">GitHub</a>. 

For general questions about this project or any ideas for academic collaboration, contact Peter Braga at: pjbraga.rubcc@gmail.com.

### Page References
<p class=reference><strong>Ambrosio, T.</strong> (2017). The fall of Yanukovych: Structural and political constraints to implementing authoritarian learning. <i>East European Politics</i>, 33(2), 184–209. Available at: <a href="https://doi.org/10.1080/21599165.2017.1304382">https://doi.org/10.1080/21599165.2017.1304382</a>.</p>
<p class=reference><strong>Government of Russia.</strong> (2020). Government of Russia: News. Available at: <a href="http://government.ru/news/">http://government.ru/news/</a>.</p>
<p class=reference><strong>Government Portal.</strong> (2017). Government Portal [Government website]. Ukrainian Government Portal. Available at: <a href="http://old.kmu.gov.ua/kmu/control/publish/">http://old.kmu.gov.ua/kmu/control/publish/</a>.</p>
<p class=reference><strong>Internet Archive.</strong> (2020). Wayback Availability JSON API. Wayback Machine. Available at: <a href="https://archive.org/help/wayback_api.php">https://archive.org/help/wayback_api.php</a>.</p>
<p class=reference><strong>Kremlin.</strong> (2020). President of Russia: Transcripts [Government website]. President of Russia. Available at: <a href="http://kremlin.ru/events/president/transcripts">http://kremlin.ru/events/president/transcripts</a>.</p>
<p class=reference><strong>Loukachevitch, N. and Levchik, A.</strong> (2016). Creating a General Russian Sentiment Lexicon. In Proceedings of Language Resources and Evaluation Conference LREC-2016. Available at: <a href="http://www.lrec-conf.org/proceedings/lrec2016/pdf/285_Paper.pdf">http://www.lrec-conf.org/proceedings/lrec2016/pdf/285_Paper.pdf</a>.</p>
<p class=reference><strong>MFA of Russia.</strong> (2020). Ministerial Speeches: Minister of Foreign Affairs of the Russian Federation. Available at: <a href="https://www.mid.ru/ru/press_service/minister_speeches/">https://www.mid.ru/ru/press_service/minister_speeches/</a>.</p>
<p class=reference><strong>Office of the Prime Minister.</strong> (2012). Archive of the Official Site of the 2008-2012 Prime Minister of the Russian Federation Vladimir Putin: Events. Available at: <a href="http://archive.premier.gov.ru/events/news/">http://archive.premier.gov.ru/events/news/</a>.</p>
<p class=reference><strong>Pavlovsky, G.</strong> (2016).</strong> Russian Politics Under Putin: The System Will Outlast the Master. <i>Foreign Affairs</i>, 95(3), 10–17. Available at: <a href="https://www.foreignaffairs.com/articles/russia-fsu/2016-04-18/russian-politics-under-putin">https://www.foreignaffairs.com/articles/russia-fsu/2016-04-18/russian-politics-under-putin</a>.</p>
<p class=reference><strong>Presidential Press Service of the Republic of Belarus.</strong> (2020). Website of the President of Belarus: Archive [Government website]. President of Belarus. Available at: <a href="http://president.gov.by/ru/news_ru/archive/page/">http://president.gov.by/ru/news_ru/archive/page/</a>.</p>
<p class=reference><strong>PyData Development Team.</strong> (2019, February 3). Pandas Documentation: Whats New in 0.24.1. Available at: <a href="https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.24.1.html">https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.24.1.html</a>.</p>
<p class=reference><strong>Reitz, K.</strong> (2019, February 18). Requests-HTML (version 0.10.0). GitHub. Available at: <a href="https://github.com/psf/requests-html">https://github.com/psf/requests-html</a>.</p>
<p class=reference><strong>Richardson, L.</strong> (2019, January 7). Beautiful Soup 4.7.1 (HTML parser). Available at: <a href="https://www.crummy.com/software/BeautifulSoup/bs4/download/4.7/">https://www.crummy.com/software/BeautifulSoup/bs4/download/4.7/</a>.</p>
<p class=reference><strong>Rudyj, K. V.</strong> (2020). “Nepohožie: Vzglâd na Kitaj i belorussko-kitajskie otnošeniâ” [<i>Dissimilar: A Perspective on China-Belarusian Relations</i>]. Zviazda: Minsk, Belarus. Available at: <a href="https://oz.by/books/more10931323.html">https://oz.by/books/more10931323.html</a>.</p>
<p class=reference><strong>Van Rossum, G., & Drake, F. L.</strong> (2018, October 20). Python 3.7.1. Available at: <a href="https://www.python.org/downloads/release/python-371/">https://www.python.org/downloads/release/python-371/</a>.</p>
