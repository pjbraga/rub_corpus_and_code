#!/usr/bin/env python3

"""preprocess_2020.py: Prepares Russian-Language sentences
                       for sentiment analysis. """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

"""
Description
    Perfoms two tasks: (1) data
    handling; (2) sentiment tagging
    (also referred to as “matching”).
    
Prerequisites
    There are two: (1) tsv column
    headings and (2) whether you
    are preprocessing a country file
    (Russia, Ukraine, Belarus) or
    a comparison country (e.g. 
    Russia and United States, or
    Belarus and Poland).
    All tsv files must have the
    following column headings:
        (1) 'id'
        (2) 'date'
        (3) 'href'
        (4) 'body'
    The 'id' column is a unqiue 
    integer for each row.
    The 'date' column has the date
    of a speech or quote, the 'href' has
    the web link to the article where 
    the politician is recorded speaking,
    and the 'body' column contains
    a sentece as a string.
    *Note: The .tsv can contain
    more than these four columns.
    However, without these four
    column headings, the code below
    WILL NOT RUN. Therefore, before
    you start, it might be wise view
    the files you are processing
    to make sure it contains these 
    four column headings.
    For comparision countries, 
    you must use the right file 
    path. See the commented out
    file paths below (which you 
    can uncomment when you need it)
    for comparision countries.

Summary of Code
    The data handling functions do 
    the following: tokenising,
    remove stopwords, lemmatisation,
    and n-gram construction.
    The sentiment tagging/matching
    functions compare two groups
    of data, (1) a list of tokenised 
    words from each sentence and
    then (2) a collection of n-grams
    up to the n-factor of six,
    against the RuSentiLex_2020.txt
    lexicon. 
    See function descriptions and
    comments below to understand
    how this script functions
"""

import codecs
import os
import pandas as pd
import re
import nltk
from nltk import ngrams
import ast
import json
from pymystem3 import Mystem
import time

# Timer
start = time.time()

# Paths
input_file = "PATH-TO-TSV-FILE-WITH-" \
    "RUSSIAN-LANGUAGE-SENTENCES."        

output_file = "PATH-TO-YET-UNMADE-OUTPUT-" \
    "FILE-TO-SAVE-YOUR-PREPROCESSING-OUTPUT"

RuSentiLex = "PATH-TO-rusentilex_2020.txt-FILE"

def main():
    # Data handling functions:
    build_output_file_main()
    view_output_file_main()
    tokenize_main()
    stop_words_main()
    lemma_list_main()
    bigrams_main()
    trigrams_main()
    quadragrams_main()
    pentagrams_main()
    hexagrams_main()
    # Matching with RuSentiLex:
    sentiment_lemma_list_main()
    sentiment_ngrams_main()
    sentiment_combined_main()

def build_output_file_main():
    """ Reads .tsv cointining
        scraped sentences.
        Creates output file.
    """

    # Views raw datafile.
    with open (input_file, \
            encoding='utf-8', mode='r') as theFile:
        fullCorpus = pd.read_csv(theFile, sep='\t')
        rows = len(fullCorpus) + 1
        print("The input file has {} rows and {} " \
                "columns.\n".format(rows, \
                len(fullCorpus.columns)))

    # Reads input file
    df = pd.read_csv(input_file, sep='\t', \
            encoding='utf-8', header=0)
    
    # Sets 'id' column as index
    df = df.set_index('id')

    # writes dataframe of input file to new output file
    df.to_csv(output_file, encoding='utf-8', sep='\t')

def view_output_file_main():
    """ Quickly checks if
        the output file has
        successfully been 
        created. 
    """

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    print("Output file built and ready.\n")

def tokenize(text):
    """ brakes sentence into 
        list of words; coded for 
        use in lambda.
    """

    tokens = re.split(r'\W+', text.lower())

    # This makes sure that nothing 
    # empty is made into a token. 
    # “filter(function, iterable) is 
    # a lambda shorthand. If I put “None”
    # in the place of “function,” it
    # checks that “for items in iterable
    # (here, iterable is “tokens”), make
    # sure there are not any NAN values. If you
    # find them, spit them out.”
    tokens1 = list(filter(None, tokens))

    return tokens1

def tokenize_main():
    """ Iterates dataframe
        with tokenize() function, 
        and writes to file.
    """

    print("Tokenising...\n")

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["body_tokenized"] = df["body"].apply(lambda x: tokenize(x))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def stop_words(token_list):
    """ Takes token_list,
        if a match is found 
        with “stopwords” list,
        the match is dropped 
        from token_list. Returns
        list.
    """

    stopwords = ['он', 'я', 'а', 'то', 'она', \
            'его', 'да', 'ты', 'у', 'были'\
            'вы', 'бы', 'ее', 'мне', \
            'вот', 'от', 'меня', 'еще', 'ему', \
            'теперь', 'когда', 'ну', 'вдруг', 'ли', \
            'уже', 'или', 'него', 'вас', \
            'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', \
            'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', \
            'есть', 'ней', 'для', 'мы', 'тебя', 'их', \
            'была', 'сам', 'чтоб', 'будто', 'чего', 'раз', \
            'тоже', 'будет', 'ж', 'тогда', 'кто', \
            'этот', 'того', 'потому', 'этого', 'какой', 'совсем', \
            'ним', 'здесь', 'этом', 'почти', 'мой', 'тем', \
            'нее', 'сейчас', 'куда', 'зачем', \
            'никогда', 'можно', 'наконец', 'два', \
            'об', 'другой', 'хоть', 'после', 'над', 'больше', \
            'через', 'эти', 'нас', 'них', \
            'какая', 'много', 'разве', 'три', 'эту', 'моя', \
            'впрочем', 'свою', 'этой', 'перед', 'иногда', \
            'лучше', 'чуть', 'нельзя', 'им', 'более', \
            'всегда', 'конечно', 'между', 'либо', 'сб']

    text = [word for word in token_list if word not in stopwords]
    
    return text

def stop_words_main():
    """ Iterates dataframe
        with stop_words(x)
        function and writes
        to file
    """

    print("Removing stop words...\n")

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["body_no_stopwords"] = \
        df["body_tokenized"].apply(lambda x: \
        stop_words(ast.literal_eval(x)))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def lemma_list(data):
    """ returns list from 
        dataframe as list of 
        lemmatized words; coded 
        for use in lambda func 
    """
    # Turn string of tokens from save file 
    # into Python recognisable list:
    text = ast.literal_eval(data)

    # Prepare for Mystem Lemmatiser:
    m = Mystem()
    sentence = " ".join(text)

    # Lemmatisation:
    lemmas = m.lemmatize(sentence)

    # Clean-up Mystem response:
    if lemmas == []:
        return ["пустая_клетка"]

    del lemmas[-1]
    lemma_sentence = "".join(lemmas)
    print(lemma_sentence)

    # Return Lemmas as a list:
    lemmaList = lemma_sentence.split(" ")
    return lemmaList

def lemma_list_main():
    """ Iterates dataframe
    with lemma_list(data)
    function and writes
    to file """

    print("Lemmatising (reducing to root form) tokenised words...\n")

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["lemma_list"] = df["body_no_stopwords"].apply(lambda \
        x: lemma_list(x)) # removed: ast.literal_eval(x)

    df.to_csv(output_file, encoding='utf-8', sep='\t')

# n-grams functions for lambda
def bigram(text):
    """ Uses nltk's ngram 
        function to make 
        a bigram of lemmatised 
        words.
    """
    ngram = list(ngrams(text, 2))
    t = tuple(" ".join(i) for i in ngram)
    
    return t

def trigram(text):
    ngram = list(ngrams(text, 3))
    t = tuple(" ".join(i) for i in ngram)
    
    return t

def quadragram(text):
    ngram = list(ngrams(text, 4))
    t = tuple(" ".join(i) for i in ngram)
    
    return t

def pentagram(text):
    ngram = list(ngrams(text, 5))
    t = tuple(" ".join(i) for i in ngram)
    
    return t

def hexagram(text):
    ngram = list(ngrams(text, 6))
    t = tuple(" ".join(i) for i in ngram)
    
    return t

# n-gram functions
def bigrams_main():
    """ Arranges Lemma_List 
        words into a bigram,
        which is ready to be 
        matched against RuSentiLex 
    """

    print("n-gram processing...\n")

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["bigrams"] = df["lemma_list"].apply(lambda \
        x: bigram(ast.literal_eval(x)))
    
    df.to_csv(output_file, encoding='utf-8', sep='\t')

def trigrams_main():
    """ Arranges Lemma_List words into a trigram,
        which is ready to be matched against RuSentiLex """

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["trigrams"] = df["lemma_list"].apply(lambda \
        x: trigram(ast.literal_eval(x)))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def quadragrams_main():
    """ Arranges Lemma_List words into a quadragram,
        which is ready to be matched against RuSentiLex """

    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["quadragrams"] = df["lemma_list"].apply(lambda \
        x: quadragram(ast.literal_eval(x)))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def pentagrams_main():
    """ Arranges Lemma_List words into a pentagram,
        which is ready to be matched against RuSentiLex """
    
    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["pentagrams"] = df["lemma_list"].apply(lambda \
        x: pentagram(ast.literal_eval(x)))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def hexagrams_main():
    """ Arranges Lemma_List words into a hexagram,
        which is ready to be matched against RuSentiLex """
    
    df = pd.read_csv(output_file, sep='\t', \
            encoding='utf-8', header=0)
    df = df.set_index('id')

    df["hexagrams"] = df["lemma_list"].apply(lambda \
        x: hexagram(ast.literal_eval(x)))
    
    df.to_csv(output_file, encoding='utf-8', sep='\t')

# RuSentiLex match for Lambda function
def extract(data):
    """ matches lemmas, extracts
        sentiment row from 
        RuSentiLex.txt file.
        See comments for detailed
        explanations of each 
        opeartion.
    """

    f = RuSentiLex

    lexicon = pd.read_csv(f, sep=',', encoding='utf-8', \
        header=None, names=['word_or_phrase', 'pos', \
        'lemma_form', 'sentiment'])

    # eval(x) is a Built-In python function that 
    # takes whatever data is given, and evaluates it
    # as a python data structure. For example, before I understood
    # how to handle JSON API responses, I used eval() as 
    # a work-around to convert the raw JSON response
    # into python, which made the response a dictionary of 
    # dictionaries (and not simply code in JSON format), 
    # which I then manually extracted data from.
    # Here, I am making sure that the list of lemmatized 
    # words being fed into this function are understood
    # as a python data, specifically as a  list. 
    # For an extra safety precaution, I am using 
    # ast.literal_eval(), which ensures no
    # malicious data can be passed into eval(). 
    info = ast.literal_eval(data)

    # If there are no 
    # sentiment bearing 
    # words (no lemmas)
    # this returns an 
    # empty list.
    if not info:
        sentiment = []
        return sentiment

    # I make the lemma list into a dataframe
    new_df = pd.DataFrame(info)
 
    # The approach I am using is what is referred 
    # to as the “Series.isin” approach. This is
    # because df['column_name'] essentially makes
    # mutable list--which is a series--out 
    # of a df column name.
    # Starting from the inside of this operation,
    # the dataframe of lemmas, “new_df[0],” is compared to the
    # 3rd column in RuSentiLex, , “lemma_form.”
    # If .isin finds a match, the entire dataframe row
    # from the “lexicon” dataframe is added to a new
    # dataframe, “match” (this is why the entire 
    # operation is wrapped in “lexicon[]”).
    match = lexicon[lexicon['lemma_form'].isin(new_df[0])]

    # The “match” dataframe, which is essentially a mini-RuSentiLex
    # constructed according the length of the list of lemmatised 
    # words, has a column containing the RuSentiLex sentiments.
    # This column of sentiments is converted into a dataframe 
    # series, whose contents are output to a basic python list,
    # “sentiment.” 
    sentiment = match['sentiment'].tolist()

    return sentiment

# Matching with RuSentiLex
def sentiment_lemma_list_main():
    """ Iterates dataset
    into extract(data)
    function """

    print("Matching lemma sentences against RuSentiLex and " \
        "attaching sentiment scores...\n")

    df = pd.read_csv(output_file, sep='\t', \
                encoding='utf-8', header=0)
    df = df.set_index('id')
    
    df['lemma_list_sentiment'] = df['lemma_list'].apply(lambda x: extract(x))

    df.to_csv(output_file, encoding='utf-8', sep='\t')
    
def sentiment_ngrams_main():
    print("Matching n-grams against RuSentiLex and " \
        "attaching sentiment scores...\n")

    df = pd.read_csv(output_file, sep='\t', \
                encoding='utf-8', header=0)

    df = df.set_index('id')
    
    df['bigrams_sentiment'] = df['bigrams'].apply(lambda x: extract(x))

    df['trigrams_sentiment'] = df['trigrams'].apply(lambda x: extract(x))

    df['quadragrams_sentiment'] = df['quadragrams'].apply(lambda x: extract(x))

    df['pentagrams_sentiment'] = df['pentagrams'].apply(lambda x: extract(x))

    df['hexagrams_sentiment'] = df['hexagrams'].apply(lambda x: extract(x))

    df.to_csv(output_file, encoding='utf-8', sep='\t')

def sentiment_combined_main():
    print("Aggregating sentence and n-gram sentiment scores...\n")

    df = pd.read_csv(output_file, sep='\t', \
                encoding='utf-8', header=0)
    df = df.set_index('id')

    data = df['lemma_list_sentiment'].apply(lambda x: ast.literal_eval(x)) \
            + df['bigrams_sentiment'].apply(lambda x: ast.literal_eval(x)) \
            + df['trigrams_sentiment'].apply(lambda x: ast.literal_eval(x)) \
            + df['quadragrams_sentiment'].apply(lambda x: ast.literal_eval(x)) \
            + df['pentagrams_sentiment'].apply(lambda x: ast.literal_eval(x)) \
            + df['hexagrams_sentiment'].apply(lambda x: ast.literal_eval(x))
    
    df['sentiment_collected'] = data

    df.to_csv(output_file, encoding='utf-8', sep='\t')
    
    print("The pre-processing code has finished " \
            "attaching sentiment tags to sentiment-" \
            "bearing words and expressions.\n\n" \
            "The output file is ready for processing " \
            "via saTagProcessor_2020.py.")

    # Print how long code takes to run:
    end = time.time()
    elapsed = end - start
    runtime = time.strftime("%j days, %H:%M:%S", time.gmtime(elapsed))
    print("\nThe code took (dd days, hh:mm:ss) {} to run.".format(runtime))

if __name__ == "__main__": main()