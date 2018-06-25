#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import unidecode
from google import google
import numpy as np
import time

################################################################################
# NLP tools
################################################################################

# NLTK
from nltk.corpus import stopwords
frenchstopwords= stopwords.words("french")
frenchstopwords.remove('qui') # qui seems to be missing from french stopwords

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
    negative_keywords = ["n'", "ne"]

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

################################################################################
# Pre/Post processing functions
################################################################################

def preprocess_question(question, lang='fra'):
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
    quote = False
    new_words = []
    for word in words:
        if word == '"':
            quote = not quote # reverse the boolean
            new_words.append(word)
            continue

        if quote:
            new_words.append(word)
            continue

        if word.lower() not in stopwords:
            new_words.append(word)

    # Concat all words to a single string again and translate to ascii lower
    question = ' '.join(new_words)
    question = unicode_to_ascii(question).lower()
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
    if lang == 'fra':
        stopwords = frenchstopwords
    else:
        stopwords = []

    if words[0].lower() in stopwords:
        del words[0]

    # Concat words back to string, transcode to ascii lower
    choice = ' '.join(words)
    choice = unicode_to_ascii(choice).lower()

    return choice

################################################################################
# Online APIs searching (Google/Wikipedia...)
################################################################################

def get_content_google(search_text):
    # Single google search
    print 'looking for:', search_text
    content = google.search(search_text, lang='en', pages=2)
    text= ''
    for page in content:
        text+= page.description + page.name

    text = text.lower()
    text = unidecode.unidecode(text)
    return text


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
    return index: index of the choosen answer, -1 if error
    """
    # Checking if question is negative or not
    is_negative = is_negative_question(question)

    # process the question and choices
    question = preprocess_question(question)
    choices = [preprocess_choice(choice) for choice in choices]

    # Get the text to search from
    content = get_content_google(question)

    # Count occurences
    counts = []
    for choice in choices:
        count = content.count(choice)
        counts.append(count)

    s = float(sum(counts))
    if s == 0:
        print 'no word found'
        return -1
    for i in range(len(counts)):
        print "%s.) %s : %.2f (%s fois)"% (i+1, choices[i], counts[i]/s, counts[i])

    # take decision
    if is_negative:
        return np.argmin(counts)
    return np.argmax(counts)
