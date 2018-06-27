#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import unidecode
from google import google
import numpy as np
import time
import string as str
from stopwords import frenchstopwords

################################################################################
# NLP tools
################################################################################

def get_n_grams(sequence, n):
    """
    Function that returns the n-grams of a sequence.
    - sequence: a list
    - n: the index of n-grams desired.
    """
    assert type(sequence) is list, 'Should be a list'
    grams = []
    for k in range(len(sequence) - n + 1):
        grams.append([sequence[i] for i in range(k, k + n)])
    return grams

def is_negative_question(question, lang='fra'):
    """
    Function to check whether the question is negative question.
    example : 'Among ..., which ... is NOT ... ?'
    - question: target question
    - lang: language of the question
    """
    if lang != 'fra':
        raise ValueError("other languages that french aren't implemented")

    # Define negative key words
    negative_keywords = ["n'"]

    if 'ne' in question.split():
        return True

    # Detect negative key words
    for negative_keyword in negative_keywords:
        if negative_keyword in question:
            print negative_keyword, question
            return True
    return False

def to_unicode(string):
    if not isinstance(string, unicode):
        return string.decode('utf-8')
    return string

def unicode_to_ascii(string):
    string = unicodedata.normalize('NFD', string).encode('ascii', 'ignore')
    return string

def get_string_type(string):
    if isinstance(string, str):
        return "ordinary string"
    if isinstance(string, unicode):
        return "unicode string"
    return "not a string"

def get_grams(string):
    # First split to words
    words = string.split()
    words = [word.lower() for word in words]
    stopwords = frenchstopwords

    n_words = []
    for word in words:
        if "'" in word:
            n_words += word.split("'")
            continue
        n_words.append(word)
    words = n_words

    # Unigrams
    unigrams = [word for word in words if word not in stopwords]

    # Bigrams
    if len(words) > 2:
        bigrams = [' '.join(bigram) for bigram in get_n_grams(words, 2)]
        n_bigrams = []
        for bigram in bigrams:
            left, right = bigram.split()
            if (left in stopwords) and (right in stopwords):
                continue
            n_bigrams.append(bigram)
        bigrams = n_bigrams
    else:
        bigrams = []

    # Initialize
    grams = {
        'unigrams' : unigrams,
        'bigrams' : bigrams,
        'complete' : [string.lower()],
    }

    return grams


################################################################################
# Pre/Post processing functions
################################################################################

def preprocess_question(question, lang='fra', delete_stopwords=False):
    """
    Preprocess the question before doing the actual research.
    Delete stopwords etc.
    - question: target question
    - lang: language of the question
    """

    # Force the question to unicode
    question = to_unicode(question)

    # Split to words
    words = question.split()

    # Replace characters using following mapping
    mapping = {
        u'\xc2\xab': '"',
        u'\xc2\xbb': '"',
        u'\xab': '"',
        u'\xbb': '"',
    }
    for i, char in enumerate(words):
        for key in mapping:
            if char == key:
                words[i] = mapping[key]

    # Get the stopwords
    stopwords = frenchstopwords if lang == 'fra' else []

    # Delete the stopwords except the ones between " "
    if delete_stopwords:
        is_quote = False
        new_words = []
        for word in words:
            if word == '"':
                is_quote = not is_quote # reverse the boolean
                new_words.append('"')
                continue

            if is_quote:
                new_words.append(word)
                continue

            if word.lower() not in stopwords:
                new_words.append(word)
        words = new_words

    # Concat all words to a single string again and translate to ascii lower
    question = ' '.join(words)
    return question

def preprocess_choice(choice, lang='fra'):
    """
    Preprocess the question before doing the actual research.
    Delete first word if it is stopword
    - question: target question
    - lang: language of the question
    """
    # Force the choice to unicode
    choice = to_unicode(choice)

    # Split to words
    words = choice.split()

    # Get the stopwords
    stopwords = frenchstopwords if lang == 'fra' else []

    if words[0].lower() in stopwords:
        del words[0]

    # Concat words back to string, transcode to ascii lower
    choice = ' '.join(words)
    choice = to_unicode(choice)
    choice = unicode_to_ascii(choice).lower()

    return choice

################################################################################
# Online APIs searching (Google/Wikipedia...)
################################################################################

def get_content_google(search_text):
    # Single google search
    print '-> Looking for in Google: %s' % (search_text)
    content = google.search(search_text, lang='en', pages=2)
    text= ''
    for page in content:
        text+= page.description + page.name

    text = text.lower()
    text = unidecode.unidecode(text)
    return text

################################################################################
# Scoring Methods
################################################################################

def simple_count(choice, content):
    """
    Simple scoring method based on preoprecessed choice occurences
    """
    # Apply a preprocessing to the choice
    choice = preprocess_choice(choice)

    # Compute the score by counting occurences
    score = content.count(choice)
    return score


def grams_count(choice, content):
    # Initialize score
    score = 0

    # Simple preprocessing
    choice = to_unicode(choice)
    choice = unicode_to_ascii(choice).lower()

    # Get n-grams as a dict
    grams = get_grams(choice)

    # Define multipliers for each gram type
    multipliers = {
        'unigrams' : 1,
        'bigrams' : 3,
        'complete' : 10,
    }

    # for each gram type
    for gram_type in grams:
        # Calculate sub score
        gram_type_score = 0
        for gram in grams[gram_type]:
            gram_type_score += content.count(gram)

        # Multiply it by the multiplier
        score += multipliers[gram_type]*gram_type_score
    return score


################################################################################
# Main Method
################################################################################

def answer(question, choices):
    """
    Answer a Multiple Choice Question (MCQ). Based on Google research, count the
    occurences of the choices, choose the choice with highest occurences, except
    if the question is negative question.
    - question: question to answer (str/unicode)
    - choices: list of choices (str/unicode)
    return index: index of the choosen answer, -1 if didn't find anything
    """
    # Checking if question is negative or not
    is_negative = is_negative_question(question)

    # process the question and choices
    question = preprocess_question(question)

    # Get the text to search from
    content = get_content_google(question)

    # Compute score for each choice
    choice_scores = []
    for choice in choices:
        # METHOD 1
        # choice_score = simple_count(choice, content)

        # METHOD 2
        choice_score = grams_count(choice, content)

        choice_scores.append(choice_score)

    NOTFOUND = False
    s = float(sum(choice_scores))
    if s == 0:
        NOTFOUND = True
        s = 1.
    print "# |conf |score"
    for i in range(len(choice_scores)):
        print "%s.)"% (i+1),
        print "%s | %s"% (choice_scores[i]/s, choice_scores[i])

    # Take final decision
    if NOTFOUND:
        return -1
    if is_negative:
        return np.argmin(choice_scores)
    return np.argmax(choice_scores)
