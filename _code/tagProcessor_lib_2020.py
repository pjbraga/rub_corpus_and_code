#!/usr/bin/env python3

""" tagProcessor_lib_2020.py: a library of functions for 
                              processing sentiment tags """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

""" 
Description
    This is a library
    file of functions 
    for “sa_tagProcessor_2020.py”.

Requirements
    The “sa_tagProcessor_2020.py”
    file.

Summary of Code
    This contains algorithms
    that “decide” the 
    sentiment of a sentence
    based on the greatest 
    fraction of sentiment
    tags out of combined
    single lemmatised words,
    and n-grams for a given
    sentence.
    It also aggregates the
    total number of positive,
    neutral, negative, and
    ambiguous sentences in
    an entire dataset, then
    uses a similar algorithm 
    to the one used for 
    sentences to decide what
    the sentiment of the
    entire dataset is. 
    This 2020 version 
    has been rewritten to 
    handle non-classifiable
    sentences.
    
Notes
    None.
"""

import os
import re
import pandas as pd
import ast

def main():
    pass

def countS(data):
    """ Adds up sentiment 
    tags in sentence from 
    preproccessed dataset. 
    That is, it shows how
    many pos, neu, neg, and
    amb tags there are
    allotted to a given  
    sentence. """

    # Note: 
    # If no match is made to RuSentiLex, the 
    # sentiment analysis codes the sentence
    # as non-classifiable, or “NotClassifiable”. 
    pattern = re.compile(r"\[\]")
    if pattern.match(data):
        data = str(['NotClassifiable'])

    t = re.split(r'\W+', data)

    pos = 0
    neg = 0
    neu = 0
    amb = 0
    nan = 0

    for elements in t:
        if elements == "positive":
            pos += 1
        if elements == "negative":
            neg += 1
        if elements == "neutral":
            neu += 1
        if elements == "positive/negative":
            amb += 1
        if elements == "NotClassifiable":
            nan += 1
    
    freq = {"positive" : pos, "negative" : neg, \
            "neutral" : neu, "ambiguous" : amb, \
            "NotClassifiable" : nan}
    return freq

def calcR(freq):
    """ Gives averages of 
    sentiment tags for 
    given sentence. Takes
    frequency counts of
    tags from countS(data) 
    and performs simple 
    division to find averages
    for each type of tag. """

    # Recognise df string as dictionary of strings
    freq = ast.literal_eval(freq)
    # convert dictionary strings to integers
    freq = dict((key,int(value)) for key, value in freq.items())

    # build denominator
    d = 0
    d += freq['positive'] + freq['negative'] \
            + freq['neutral'] + freq['ambiguous']
    if d == 0:
        d = 1
    # calculate ratios
    rpos = freq['positive'] / d
    rneg = freq['negative'] / d
    rneu = freq['neutral'] / d
    ramb = freq['ambiguous'] / d
    rnan = freq['NotClassifiable'] / 1
    # dictionary of ratios
    ratios = {"positive" : rpos, "negative" : rneg, \
        "neutral" : rneu, "ambiguous" : ramb, \
        "NotClassifiable" : rnan}
    return ratios

def maxS(ratios):
    """ Finds the greatest ratio
    value, or triggers rules,
    to decide sentiment for each
    sentence. This is the main
    “algorithm” of the sentiment 
    analysis. It is the simple
    decision tree that concludes
    what sentiment a sentence 
    has. """

    # Converts ratios from dataframe
    # into dictionary with integer values
    ratios = ast.literal_eval(ratios)
    ratios = dict((key,float(value)) for key, value in ratios.items())

    # Finds which of the sentiment
    # ratios is greatest in the dictionary
    sentiment = max(ratios, key=ratios.get)

    # This checks if more than one sentiment
    # share the same ratio
    ratio = ratios[sentiment]
    trigger = []
    for keys, values in ratios.items():
        if ratio == values:
            trigger.append(keys)

    # If sentiment ratios are the same, 
    # the following rules are triggered
    if len(trigger) > 1:
        if ratios["positive"] == ratios["negative"]:
            sentiment = "ambiguous"
        if ratios["positive"] == ratios["neutral"] or ratios["ambiguous"]:
            sentiment = "positive"
        if ratios["negative"] == ratios["neutral"] or ratios["ambiguous"]:
            sentiment = "negative"
        if ratios["neutral"] == ratios["ambiguous"]:
            sentiment = "ambiguous"
        if ratios["positive"] == ratios["negative"] == ratios["neutral"] == ratios["ambiguous"]:
            sentiment = "ambiguous"
    
    return sentiment

def corpusCount(data):
    """ Adds up computed sentiment 
    from file containing dictonary
    of corpus sentiment scores. That
    is, like countS(data), this
    function merely counts all
    the sentiment tags decided 
    by maxS(ratios), but for the
    totality of all collected 
    sentences (of the corpus). """

    corpus = ast.literal_eval(data)

    pos = 0
    neg = 0
    neu = 0
    amb = 0
    nan = 0

    for keys, values in corpus.items():
        if values == "positive":
            pos += 1
        if values == "negative":
            neg += 1
        if values == "neutral":
            neu += 1
        if values == "ambiguous":
            amb += 1
        if values == "NotClassifiable":
            nan += 1
    
    scores = {"positive" : pos, "negative" : neg, \
                "neutral" : neu, "ambiguous" : amb, \
                "NotClassifiable" : nan}
    
    return scores

def endRatio(freq):
    """ Takes frequncies of corpus
    sentiments and calculates
    averages of each sentiment. 
    Again, like calcR(freq) above,
    this uses simple division to
    find average sentiment tag 
    counts, but it does so 
    for the entire corpus (all
    sentences as a collective whole).
    """

    # Recognise df string as dictionary of strings
    freq = ast.literal_eval(freq)
    # convert dictionary strings to integers
    freq = dict((key,int(value)) for key, value in freq.items())
    # build demoninator
    d = 1
    d += freq['positive'] + freq['negative'] \
            + freq['neutral'] + freq['ambiguous']
    # calculate ratios
    rpos = freq['positive'] / d
    rneg = freq['negative'] / d
    rneu = freq['neutral'] / d
    ramb = freq['ambiguous'] / d
    rnan = freq['NotClassifiable'] / 1
    # dictionary of ratios
    ratios = {"positive" : rpos, "negative" : rneg, \
        "neutral" : rneu, "ambiguous" : ramb, \
        "NotClassifiable" : rnan}

    return ratios

def finalMax(freq):
    """ This function uses
    a set of rules to decide 
    which sentiment defines
    the corpus. This last 
    algorithm gives the 
    overall sentiment of 
    the corpus (total 
    collection of sentences). 
    """

    # Recognise df string as dictionary of strings
    freq = ast.literal_eval(freq)
    # convert dictionary strings to integers
    freq = dict((key,int(value)) for key, value in freq.items())

    sentiment = max(freq, key=freq.get)
    score = freq[sentiment]
    # This checks if more than one sentiment
    # share the same score.
    trigger = []
    for keys, values in freq.items():
        if score == values:
            trigger.append(keys)

    # If sentiment scores are the same, 
    # the following rules are triggered.
    if len(trigger) > 1:
        if freq["positive"] == freq["negative"]:
            sentiment = "ambiguous"
        if freq["positive"] == freq["neutral"] or freq["ambiguous"]:
            sentiment = "positive"
        if freq["negative"] == freq["neutral"] or freq["ambiguous"]:
            sentiment = "negative"
        if freq["neutral"] == freq["ambiguous"]:
            sentiment = "ambiguous"
        if freq["positive"] == freq["negative"] == freq["neutral"] == freq["ambiguous"]:
            sentiment = "ambiguous"
    
    return sentiment

if __name__ == "__main__": main()