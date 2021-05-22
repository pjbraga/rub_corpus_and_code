# The RUB Corpus and Code

### Russian-Language Corpus & Lexicon-Based Sentiment Analysis

![Corpus Organisation](/images/corpus_org.png)

![The Code](/images/code_example.png)

RUB Corpus and Code are two downloadable, open-source collections. 

The [RUB Corpus](https://github.com/pjbraga/rub_corpus_and_code/tree/main/_corpus) is a collection of Russian-language official government speeches, interviews, and press releases made by top policymakers in Russia, Ukraine, and Belarus from 2006 to 2016.

The first image at the top of this README is a screenshot of the corpus collection for Belarus.

The [Code](https://github.com/pjbraga/rub_corpus_and_code/tree/main/_code) represents the programs used to compile the RUB Corpus and to conduct a lexicon-based sentiment analysis upon the RUB Corpus.

The second image above is a screenshot of a lemmatisation function, which is part of the sentiment analysis Code.

The sentiment analysis was conducted using a modified version of the lexicon created by [Loukachevitch and Levchik (2016)](http://www.labinform.ru/pub/rusentilex/index.htm).

# Usage
To use any of the RUB Code scripts, please use the following citation:

<strong>Braga, P.</strong> (2020). RUB Corpus and Code. Project repository. Available at:<a href="https://github.com/pjbraga/rub_corpus_and_code"> https://github.com/pjbraga/rub_corpus_and_code</a>. 

### The RUB Corpus Files
The RUB Corpus and Code can be used in several ways. 

[The corpus](https://github.com/pjbraga/rub_corpus_and_code/tree/main/_corpus) is a collection of 71,515 Russian-language texts published
between 01 January 2006 to 31 December 2016.

The Corpus is divided by country (russia_all_texts.tsv.zip, ukraine_all_texts.tsv.zip, belarus_all_texts.tsv.zip) in plain text .tsv (tab-separated values) files.

The Corpus files can be utilised by any language that is suitable for text-processing and data-handling of .tsv files (such as python or Perl).

The sources for the RUB Corpus texts are online, official government archives. Therefore, the data is already within the public domain and can be used however the user sees fit.

### The Code (Sentiment Analysis) Files
[The Code](https://github.com/pjbraga/rub_corpus_and_code/tree/main/_code) is a series of programs used to: 

(1) assemble the [RUB Corpus](https://github.com/pjbraga/rub_corpus_and_code/tree/main/_corpus) and; 
(2) conduct a Russian-language, lexicon-based, sentiment analysis upon the RUB Corpus. 

All the Code scripts are writtin in [python](https://docs.python.org/3/).

Thus, to use the Code, it is necessary to have some basic knowledge of python and certain site-packages (such as pandas, the natural language toolkit, beautiful-soup, etc...) associted with it.

In addition, considering this code deals with Russian-language texts, it helps to have some knowledge of Russian as well. 

The various .py (python) scripts contain multiple notes and comments, which are intended to make the code easier to understand.

All the scripts uploaded here begin with a strandard file header, and then a comment block of four headings:
- Description (a one-to-two sentence explanation of the script)
- Requirements (necessary prerequisites to run the script)
- Summary of Code (synopsis of the layout and function of the script)
- Notes (any peculiarities or potential issues with the code)

# Reporting Issues
For any issues with the RUB Corpus and Code repositories, please use <a href="https://github.com/pjbraga/rub_corpus_and_code">GitHub</a>. 

# Contact
For general questions about this project or any ideas for academic collaboration, contact Peter Braga at: pjbraga.rubcc@gmail.com.