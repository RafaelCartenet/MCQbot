import random
import unicodedata
import unidecode
from google import google
import numpy as np
import time


# NLTK
from nltk.corpus import stopwords
frenchstopwords= stopwords.words("french")
frenchstopwords.remove('qui')

def to_ascii(string):
    # string = unicode(string,'utf-8')
    # string = unicodedata.normalize('NFD', string).encode('ascii', 'ignore')

    return unidecode.unidecode(string)
    return string

def preprocessing_question(question, lang='fra'):
    # Split words
    words = question.split()

    # Get the stopwords
    if lang == 'fra':
        stopwords = frenchstopwords
    else:
        stopwords = []

    # Delete the stopwords
    quote = False
    n_words = []
    for word in words:
        if word == '"':
            if quote == False:
                quote = True
            elif quote == True:
                quote = False
            n_words.append(word)
            continue

        if quote:
            n_words.append(word)

        else:
            if word.lower() not in stopwords:
                n_words.append(word)

    # Concat all words to a single sentence again
    question = ' '.join(n_words)

    # Convert to ascii
    question = to_ascii(question)

    return question

def preprocessing_choice(choice, lang='fra'):
    words = choice.split()

    # print 'BEFORE', choice
    # Get the stopwords
    if lang == 'fra':
        stopwords = frenchstopwords
    else:
        stopwords = []

    if words[0].lower() in stopwords:
        del words[0]

    choice = ' '.join(words)
    choice = to_ascii(choice).lower()

    return choice


def get_n_grams(sequence, n):
    assert type(sequence) is list, 'Should be a list'

    grams = []
    for k in range(len(sequence) - n + 1):
        grams.append([sequence[i] for i in range(k, k + n)])

    return grams

def is_negative_question(question, lang='fra'):
    if lang != 'fra':
        raise ValueError('other languages that french not implemented')

    # Detect negation key words
    if (" n'" in question) or (' ne ' in question):
        return True
    return False

def postprocessing_text(text):
    # split to list of words
    text = to_ascii(text)
    text = text.split()
    return text

def answer(question, choices):
    is_interonegative = is_negative_question(question)

    # process the question and choices
    question= preprocessing_question(question)
    choices= [preprocessing_choice(choice) for choice in choices]

    # Single google search
    t = time.time()
    pages= google.search(question, lang='en', pages=2)
    #
    print 'looking for:', question
    request_time = time.time() - t

    # Get the text to search from
    text= ''
    for page in pages:
        text+= page.description + page.name
    text = text.lower()
    text = unidecode.unidecode(text)

    # Count occurences
    counts = []
    for choice in choices:
        count = text.count(choice)
        counts.append(count)

    s = float(sum(counts))
    if s == 0:
        print 'no word found'
        # Take random decision
        return random.randint(0, len(choices))

    for i in range(len(counts)):
        print "%s.) %s : %.2f (%s fois)"% (i+1, choices[i], counts[i]/s, counts[i])

    # take decision
    if is_interonegative:
        return np.argmin(counts)
    return np.argmax(counts)
