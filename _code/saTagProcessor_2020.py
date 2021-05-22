#!/usr/bin/env python3

""" saTagProcessor_2020.py: After preprocessing, this
                            uses an algorithm to decide
                            the sentiment of lexicon
                            tagged sentences. """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

"""
Description
    Uses a simple algorithm 
    (from a library file) to
    calculate the sentiment of 
    a given text or series of 
    texts, which have been 
    prepared (preprocessed) 
    beforehand. 

Requirements
    (1) input file must have been
        preprocessed.
    (2) Remember to use correct
        file paths for analysis
        countries and comparsion
        countries--see commented-
        out code below.

Summary of code
    Writes three additional columns
    to the input file, and then
    a new, three column dataframe
    to an output file.

    The code here primaliry writes
    dataframes to files. The code
    that does the sentiment analysis
    (or, rather, the calculating
    of the sentiment tags) is 
    in a library file (identified
    by the “_lib.py” in its file
    name).

    This 2020 version has been
    updated to include non-classifiable
    sentences.
"""

import codecs
import re
import pandas as pd
import ast
import time

# The following import is a 
# series of custom functions
# placed in a separate .py file,
# so the code in this file is less
# verbose.
import tagProcessor_lib_2020 as tp

# Timer
start = time.time()

# File Paths:

input_file = "PATH-TO-YOUR-PREPROCESSED-" \
    "SENTENCES-FILE.TSV"

output_file = "PATH-TO-WHERE-YOU-WANT-TO-" \
    "SAVE-YOUR-RESULTS.TSV"

def main():
    view_input_file()
    sentimentFreq()
    sentimentRatios()
    sentiment()
    corpus()
    corpusFreq()
    display()

def view_input_file():
    """ Takes a quick look 
    at dataset """

    # Views raw datafile.
    with open (input_file, \
        encoding='utf-8', mode='r') as theFile:
        df = pd.read_csv(theFile, sep='\t', \
            encoding='utf-8', header=0)
        rows = len(df) + 1
        print("The input file has {} rows and {} " \
                "columns.\n".format(rows, \
                len(df.columns)))
        # print(df.head)

def sentimentFreq():
    """ Executes countS() from 
    tagProcessor_lib, and writes 
    results to input file """

    df = pd.read_csv(input_file, sep='\t', encoding='utf-8', header=0)

    df["frequency"] = df["sentiment_collected"].apply(lambda x: tp.countS(x))

    df.to_csv(input_file, encoding='utf-8', sep='\t', index=False)

def sentimentRatios():
    """ Executes calcR() from
    tagProcessor_lib, and writes 
    results to input file """

    df = pd.read_csv(input_file, sep='\t', encoding='utf-8', header=0)

    df["ratios"] = df["frequency"].apply(lambda x: tp.calcR(x))

    df.to_csv(input_file, encoding='utf-8', sep='\t', index=False)

def sentiment():
    """ Executes maxS() from 
    tagProcessor_lib and writes 
    results to input file """

    df = pd.read_csv(input_file, sep='\t', encoding='utf-8', header=0)

    df["sentiment"] = df["ratios"].apply(lambda x: tp.maxS(x))

    df.to_csv(input_file, encoding='utf-8', sep='\t', index=False)

def corpus():
    """ From input file,
    this makes a dictionary with 
    sentence id number as key, 
    and the sentiment result as
    value. Writes dictionary to 
    separate output file """

    df = pd.read_csv(input_file, sep='\t', encoding='utf-8', header=0)

    corpus = pd.Series(df.sentiment.values, index=df.id).to_dict()

    sentenceResults = open(output_file, encoding='utf-8', mode='w+')
    sentenceResults.write(str(corpus))
    sentenceResults.close()

def corpusFreq():
    """ Opens output file to access
    dictionary of results, calls 
    corpusCount(data) from 
    tagProcessor_lib and writes 
    results as a dataframe to same
    output file """

    with open(output_file, encoding='utf-8', mode='r') as theFile:
        data = theFile.read()
    
    df = pd.read_csv(output_file, sep='\t', encoding='utf-8', \
            header=None, names=["sentence_scores"])
    df["corpus_scores"] = pd.Series([tp.corpusCount(data)])

    df.to_csv(output_file, encoding='utf-8', sep='\t', index=False)

def display():
    """ Accesses cumulative corpus
    sentiment frequency from 
    results file. Calls tp.endRatio(freq)
    from tagProcessor_lib to calculate
    corpus sentiment averages. Calls
    tp.finalMax(freq) to compute 
    overall corpus sentiment. Writes
    to output file """

    df = pd.read_csv(output_file, sep='\t', encoding='utf-8', \
            header=0)
    freq = df.at[0, "corpus_scores"]

    ratios = tp.endRatio(freq)
    p = ratios["positive"] * 100
    neg = ratios["negative"] * 100
    neu = ratios["neutral"] * 100
    a = ratios["ambiguous"] * 100
    nan = ratios["NotClassifiable"]

    sentiment = tp.finalMax(freq)
    result = "\nThe corpus has an overall {} sentiment. " \
                "\nThe corpus contains the following polarity: " \
                "\n\t{} percent positive; \n\t{} percent negative; " \
                "\n\t{} percent neutral; \n\tand {} percent ambiguous." \
                .format(sentiment, p, neg, neu, a)
    
    # Writes above results to output file
    df = pd.read_csv(output_file, sep='\t', encoding='utf-8', \
            header=0)
    df["result"] = pd.Series([result])
    df.to_csv(output_file, encoding='utf-8', sep='\t', index=False)
    
    # View results in terminal:
    df = pd.read_csv(output_file, sep='\t', encoding='utf-8', \
            header=0)

    # prints raw scores
    score = df.at[0, "corpus_scores"]
    print("Raw Scores:")
    print(score)

    # Classifable vs. Non-Classifiable Sentences
    # Get summary of classified senteces from results file
    score = ast.literal_eval(df.at[0, "corpus_scores"])
    # Convert numbers within dictionary to integers,
    # but keeping keys as strings.
    score = dict((key,float(value)) for key, value in score.items())
    # define sentence type scores
    pos = score["positive"]
    neg = score["negative"]
    neu = score["neutral"]
    amb = score["ambiguous"]
    nan = score["NotClassifiable"]
    tSentences = pos+neg+neu+amb+nan
    classifiable = pos+neg+neu+amb
    nonClassifiable = nan
    print("\nThe RuSentiLex_2020 Lexicon processed " \
            "a total of {} sentences." \
            "\nThe sentence frequencies are:" \
            "\n\tPositive = {}" \
            "\n\tNegative = {}" \
            "\n\tNeutral = {}" \
            "\n\tAmbiguous = {}" \
            "\n\nRuSentiLex_2020 managed to classify {} sentences." \
            "\nIt failed to classify {} sentences." \
            .format(tSentences, pos, neg, neu, amb, \
                classifiable, nonClassifiable))

    # Prints out the “result” column from .tsv result file
    check = df.at[0, "result"]
    print(check)

    # Print how long code takes to run:
    end = time.time()
    elapsed = end - start
    runtime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    print("\nThe code took (hh:mm:ss) {} to run.".format(runtime))

if __name__ == "__main__": main()