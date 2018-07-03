#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Rafael Cartenet. 2018

from stopwords import frenchstopwords
from google import google
import numpy as np
import unicodedata
import time


################################################################################
# NLP tools
################################################################################

def get_n_grams(sequence, n):
    """
    Function that returns the n-grams of a sequence.
    - sequence: a list
    - n: the index of n-grams desired.
    """
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

    # Define negative patterns
    negative_patterns = [" n'", " ne "]

    # Detect negative patterns
    for negative_pattern in negative_patterns:
        if negative_pattern in question:
            return True
    return False

def correct_unknown_chars(string):
    """
    Some characters have different possibilities, according to language, such as
    apostrophes or quotes. We make sure to transcode them to a common value.
    - string: unicode string to be corrected
    """
    # Create the reverse mapping
    reverse_mapping = {
        "'": [u'‘', u'’'], # apostrophes
        '"': [u'«', u'»', u'‹', u'›', u'“', u'”'] # quotes
    }
    # Generate the original mapping by reversing the reverse mapping
    mapping = dict()
    for key in reverse_mapping:
        for item in reverse_mapping[key]:
            mapping[item] = key

    # Replace chars using the mapping
    string = reduce(lambda x, y: x.replace(y, mapping[y]), mapping, string)
    return string

def get_grams(string):
    """
    From a given string, extract the unigrams and the bigrams, postprocess them
    and return them in a dict structure.
    Post processing includes incorrect grams deletion etc.
    - string: a string
    return: grams. Structure containing unigrams, bigrams and complete string.
    """
    # First split to words
    words = string.split()
    words = [word.lower() for word in words]
    stopwords = frenchstopwords

    # Split string to words, smartly
    n_words = []
    for word in words:
        # if word contains apostroph, split it to two parts
        if "'" in word:
            n_words += word.split("'")
            continue

        n_words.append(word)
    words = n_words

    # UNIGRAMS
    unigrams = [word for word in words if word not in stopwords]

    # BIGRAMS
    bigrams = []
    if len(words) > 2:
        # get bigrams
        raw_bigrams = get_n_grams(words, 2)

        # raw_bigrams post processing
        bigrams = []
        for bigram in raw_bigrams:
            left, right = bigram

            # if every word of the bigram is a stopword, we ignore it.
            if (left in stopwords) and (right in stopwords):
                continue

            # join the bigram as a single string
            bigrams.append(' '.join(bigram))

    # Create our grams structure
    grams = {
        'unigrams' : unigrams,
        'bigrams' : bigrams,
        'complete' : [preprocess_choice(string)],
    }
    return grams


################################################################################
# Ascii/Unicode conversions
################################################################################

def to_unicode(string):
    """
    Force bytes string to unicode
    - string: any string
    """
    if not isinstance(string, unicode):
        return string.decode('utf-8')
    return string

def unicode_to_ascii(string):
    """
    Transform unicode string to ascii string
    - string: unicode string
    """
    string = unicodedata.normalize('NFD', string).encode('ascii', 'ignore')
    return string


################################################################################
# Pre/Post processing functions
################################################################################

def preprocess_question(question, lang='fra', delete_stopwords=True):
    """
    Preprocess the question before doing the actual research.
    Delete stopwords etc.
    - question: target question
    - lang: language of the question
    """
    # Split to words
    words = question.split()

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
    """
    Google research, using google API. Get the first two pages of research,
    extract the description of the different items as well as the title names.
    """
    # Single google search
    content = google.search(search_text, lang='en', pages=2)

    # Concat all text together as a single string
    text= ''
    for page in content:
        text+= page.description + page.name

    # Post processing, transcode to ascii lower
    text = unicode_to_ascii(text).lower()
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
    """
    Scoring method based on n-grams. Preprocess the choice, get the unigrams,
    bigrams of the choice. Count then in the content and compute finale score.
    Final score is the sum of the occurences multiplied by a factor.
    score = k1 x occ_unigrams + k2 x occ_bigrams + k3 x occ_complete
    - choice: string, one possible choice for the answer
    - content: string, content to search from.
    """
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
# Main Methods
################################################################################

def answer_scores(question, choices, method='ngrams_counts'):
    """
    Estimates score of each choice of a Multiple Choice Question (MCQ).
    Based on Google research, compute score for each choice based on different
    methods.
    - question: question to answer (str/unicode)
    - choices: list of choices (str/unicode)
    return index: score of each choice, all sum to 1. If nothing was found,
    returns list of zeros of size len(choices).
    """
    # Force the question to unicode
    question = to_unicode(question)

    # Replace unknown unicode characters
    question = correct_unknown_chars(question)

    # Checking if question is negative or not
    is_negative = is_negative_question(question)

    # Process the question
    question = preprocess_question(question)

    # Get the text to search from
    content = get_content_google(question)

    # Compute score for each choice, based on method
    choice_scores = []
    for choice in choices:
        # METHOD 1 (simple counting)
        if method == 'simple_counts':
            choice_score = simple_count(choice, content)
            choice_scores.append(choice_score)
            continue

        # METHOD 2 (n-grams weighted counting)
        if method == 'ngrams_counts':
            choice_score = grams_count(choice, content)
            choice_scores.append(choice_score)
            continue

        # method is unknown
        raise ValueError('Unkonwn scoring method for scoring.')

    # Sum of all scores
    sum_ = float(sum(choice_scores))

    # That means nothing was found, we return a list of zeros
    if sum_ == 0:
        return choice_scores

    # Revert score if it is negative
    if is_negative:
        # Invert scores
        max_score = max(choice_scores)
        choice_scores = [max_score - score for score in choice_scores]

        # Update the sum of all scores
        sum_ = float(sum(choice_scores))

    # Softmax (Divide by sum each element so that sum of list is 1)
    choice_scores = [choice_score/sum_ for choice_score in choice_scores]
    return choice_scores

def answer(question, choices):
    """
    Based on the scores of each choice, take a decision about which choice to
    take.
    - question: question to answer (str/unicode)
    - choices: list of choices (str/unicode)
    return index: index of the choosen choice
    """
    # Get the score of each choice of the question
    choice_scores = answer_scores(question, choices)

    # If sum equals = 0 means all score are zeros means we didn't find anything
    if sum(choice_scores) == 0:
        return -1

    # Return the index of the highest score
    index = np.argmax(choice_scores)
    return index
