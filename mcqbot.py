import random
import unicodedata
import unidecode
from google import google
import numpy as np
import time

def to_ascii(string):
    s1 = unicode(string,'utf-8')
    s2 = unicodedata.normalize('NFD', s1).encode('ascii', 'ignore')
    return s2

def preprocessing_question(question):
    # Convert to ascii characters
    question= to_ascii(question)
    return question


def answer(question, choices):
    # process the question and choices
    question= preprocessing_question(question)
    choices= [to_ascii(choice).lower() for choice in choices]

    # Single google search
    t = time.time()
    pages= google.search(question, pages=3)
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
        'no word found'
        return random.randint(0, len(choices))

    for i in range(len(counts)):
        print "%s.) %s : %.2f (%s fois)"% (i+1, choices[i], counts[i]/s, counts[i])

    # take decision
    return np.argmax(counts)
