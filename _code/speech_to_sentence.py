#!/usr/bin/env python3

""" speech_to_sentence.py: This breaks larger texts
                           into single sentences for 
                           structuring data for sentiment
                           analysis. """

__author__ = "Peter Braga"
__copyright__ = "Copyright 2021, Peter Braga"
__credits__ = ["Peter Braga"]
__maintainer__ = "Peter Braga"
__email__ = "pjbraga.rubcc@gmail.com"

""" 
Description
    This code prepares internet 
    scraped text in a .tsv file 
    for sentiment analysis 
    pre-proccessing.

Requirements
    (1) input file must be .tsv or .csv file
    (2) first line of .tsv file must 
        contain the following: 
        date	href	text

Summary of code
    .tsv file is read as a pandas
    dataframe, df.
    
    A regex function, match(), 
    scans the “text” column for
    sentences containing an 
    adjective describing a country. 
    
    Full sentences in the speech 
    column are extracted into 
    a list. This list of sentences 
    is placed into a new column, 
    "sentences".
    
    The speech column is deleted.
    
    Each sentence within the list 
    of sentences is “exploded.” 
    This means each sentence in the
    list of sentences is given its 
    own dataframe row under the 
    “sentences” column.
    Finally, the dataframe is 
    written to an output .tsv file.

"""

import os
import codecs
import re
import pandas as pd
import ast


# file paths:
input_file = "PATH-TO-YOUR-TSV-FILE-" \
    "OF-RUSSIAN-LANGUAGE-TEXTS.TSV"

output_file = "PATH-TO-WHERE-YOU-" \
    "WANT-TO-SAVE-YOUR-TEXT-SENTENCES.TSV"


def main():
    speech_to_sentence()

def matcher(data):
    """ Matches adjective of
        a country within a 
        given sentence. Places
        Sentences into a list.
    """
    # Adjectives of countries
    # China:
    # pattern = re.compile(r'[^?!.]*китай[^?!.]*|[^?!.]*\bкита[^?!.]*|[^?!.]*\bкнр\b[^?!.]*', \
    #     flags=re.I)

    # Belarus Comaprison Countries
    # Poland:
    # pattern = re.compile(r'[^?!.]*польша[^?!.]*|[^?!.]*\bпольск[^?!.]*|[^?!.]*\bпольш[^?!.]*', \
    #     flags=re.I)
    # Uzbekistan:
    # pattern = re.compile(r'[^?!.]*узбекистан[^?!.]*|[^?!.]*\bузбек[^?!.]*', \
    #     flags=re.I)
    # Venezuela
    # pattern = re.compile(r'[^?!.]*венесуэл[^?!.]*', \
    #     flags=re.I)
    # Armenia
    # pattern = re.compile(r'[^?!.]*\bармяни[^?!.]*|[^?!.]*\bармянск[^?!.]*', \
    #     flags=re.I)
    # India
    # pattern = re.compile(r'[^?!.]*\bиндия[^?!.]*|[^?!.]*\bиндийск[^?!.]*|[^?!.]*\bиндии[^?!.]*', \
    #     flags=re.I)
    
    # Russia Comparison Countries
    # Finland
    # pattern = re.compile(r'[^?!.]*финляндия[^?!.]*|[^?!.]*\bфинск[^?!.]*|[^?!.]*\bфинлянд[^?!.]*', \
    #     flags=re.I)
    # Italy
    # pattern = re.compile(r'[^?!.]*\bитали[^?!.]*|[^?!.]*\bиталь[^?!.]*', \
    #     flags=re.I)
    # Mongolia
    # pattern = re.compile(r'[^?!.]*\bмонгол[^?!.]*|[^?!.]*\bмнр\b[^?!.]*', \
    #     flags=re.I)
    # United States
    # pattern = re.compile(r'[^?!.]*соединённые штаты америки[^?!.]*|[^?!.]*\bштаты[^?!.]*|[^?!.]*\bсша\b[^?!.]*|[^?!.]*\bамерик[^?!.]*', \
    #     flags=re.I)
    # Germany
    # pattern = re.compile(r'[^?!.]*\bгермани[^?!.]*|[^?!.]*\bнемецк[^?!.]*|[^?!.]*\bфрг\b[^?!.]*|[^?!.]*\bнемц[^?!.]*|[^?!.]*\bнемец\b[^?!.]*', \
    #     flags=re.I)
    # Netherlands
    # pattern = re.compile(r'[^?!.]*\bнидерланд[^?!.]*|[^?!.]*\bголланд[^?!.]*', \
    #     flags=re.I)
    # European Union
    # pattern = re.compile(r'[^?!.]*\bевропейск[^?!.][^?!.][^?!.] союз[^?!.]*|[^?!.]*\bевропейск[^?!.][^?!.] союз[^?!.]*|[^?!.]*\bес\b[^?!.]*|[^?!.]*\bевросоюз[^?!.]*', \
    #    flags=re.I)

    # Ukrane Comparison Countries
    # Estonia
    # pattern = re.compile(r'[^?!.]*\bэстон[^?!.]*', \
    #     flags=re.I)
    # Finland
    # pattern = re.compile(r'[^?!.]*финляндия[^?!.]*|[^?!.]*\bфинск[^?!.]*|[^?!.]*\bфинлянд[^?!.]*', \
    #     flags=re.I)
    # Latvia
    # pattern = re.compile(r'[^?!.]*\bлатви[^?!.]*|[^?!.]*\bлатышск[^?!.]*|[^?!.]*\bлатвийск[^?!.]*', \
    #     flags=re.I)
    # Russia
    # pattern = re.compile(r'[^?!.]*\bрусск[^?!.]*|[^?!.]*\bросси[^?!.]*|[^?!.]*\bрф\b[^?!.]*', \
    #     flags=re.I)
    # Georgia
    # pattern = re.compile(r'[^?!.]*\bгрузи[^?!.]*|[^?!.]*\bгрузинск[^?!.]*', \
    #     flags=re.I)
    # Kazakhstan
    # pattern = re.compile(r'[^?!.]*казахстан[^?!.]*', \
    #     flags=re.I)
    # Turkey
    # pattern = re.compile(r'[^?!.]*\bтурци[^?!.]*|[^?!.]*\bтурецк[^?!.]*', \
    #     flags=re.I)

    # Word Search
    # pattern = re.compile(r'[^?!.]*\bзон[^?!.]*', \
    #     flags=re.I)
    # pattern = re.compile(r'[^?!.]*\bсуверенитет[^?!.]*', \
    #     flags=re.I)
    # pattern = re.compile(r'[^?!.]*\bсталин\b[^?!.]*|[^?!.]*\bсталин[^?!.]\b[^?!.]*|[^?!.]*\bсталин[^?!.][^?!.]\b[^?!.]*|[^?!.]*\bсталин[^?!.][^?!.][^?!.]\b[^?!.]*', \
    #     flags=re.I)
    # pattern = re.compile(r'[^?!.]*\bсоветск[^?!.][^?!.][^?!.] союз[^?!.]*|[^?!.]*\bсоветск[^?!.][^?!.] союз[^?!.]*|[^?!.]*\bссср\b[^?!.]*', \
    #     flags = re.I)
    # pattern = re.compile(r'[^?!.]*\bсвобод\b пресс[^?!.]*|[^?!.]*\bсвобод[^?!.]\b пресс[^?!.]*|[^?!.]*\bсвобод[^?!.][^?!.]\b пресс[^?!.]*|[^?!.]*\bсвобод[^?!.][^?!.][^?!.]\b пресс[^?!.]*|[^?!.]*\bсвобод[^?!.]\b слов[^?!.]*|[^?!.]*\bсвобод[^?!.]\b печат[^?!.]*', \
    #     flags = re.I)
    pattern = re.compile(r'[^?!.]*\bдемократи[^?!.]\b[^?!.]*|[^?!.]*\bдемократи[^?!.][^?!.]\b[^?!.]*|[^?!.]*\bдемократи[^?!.][^?!.][^?!.]\b[^?!.]*', \
        flags = re.I)
    # pattern = re.compile(r'[^?!.]*\bправ\b женщи[^?!.]*|[^?!.]*\bправ[^?!.]\b женщи[^?!.]*|[^?!.]*\bправ[^?!.][^?!.]\b женщи[^?!.]*|[^?!.]*\bравноправи[^?!.]\b женщи[^?!.]*|[^?!.]*\bравноправи[^?!.][^?!.]\b женщи[^?!.]*|[^?!.]*\bравноправи[^?!.][^?!.][^?!.]\b женщи[^?!.]*|[^?!.]*\bфеминизм\b[^?!.]*|[^?!.]*\bфеминизм[^?!.]\b[^?!.]*|[^?!.]*\bфеминизм[^?!.][^?!.]\b[^?!.]*', \
    #     flags = re.I)

    sentences = re.findall(pattern, str(data))

    return sentences

def speech_to_sentence():
    # locate and open file with date/href/speech columns
    print("Locating and loading input file...")
    with open(input_file, newline="", encoding='utf-8', \
        mode='r') as theFile:
        df = pd.read_csv(theFile, sep='\t', header=0)
    print("File loaded.")
    
    # Regex searches the speeches using lambda and matcher()

    print("Searching for sentences that mention target country...")
    df["sentences"] = df["text"].apply(lambda x: \
        matcher(x))
    print("Search finished.")

    # Delete the speech column, so file is smaller
    df = df.drop(['text'], axis=1)
    
    # Expand the list of sentences into single dataframe rows,
    # but making sure the correct date and href point
    # to the sentence where it came from.
    # Otherwise referred to “exploding nested lists.”
    print("Exploding nested lists containing individual sentences...")
    df = df.set_index(['date', 'href']).sentences.apply(pd.Series).stack()\
        .reset_index(name = 'sentences').drop('level_2', axis = 1)

    # Remove any duplicates
    print("Removing duplicates...")
    df.drop_duplicates(subset=['sentences'], keep='first', inplace=True)
    print("Reindexing...")
    df = df.reset_index(drop=True)

    # Write to file
    print("Writing output file...")
    df.to_csv(output_file, encoding='utf-8', sep='\t')

    print("Process complete.")

if __name__ == "__main__": main()