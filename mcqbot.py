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

def answer_v1(question, choices):
    my_answer= random.choice(choices)
    question= to_ascii(question)

    choices= [to_ascii(choice).lower() for choice in choices]

    t = time.time()
    pages= google.search(question, pages=3)
    request_time = time.time() - t

    text= ''

    for page in pages:
        text+= page.description + page.name


    text = text.lower()
    text = unidecode.unidecode(text)

    counts = []

    for choice in choices:
        count = text.count(choice)
        counts.append(count)

    s = float(sum(counts))
    print '\nQUESTION: %s (google search time: %.2fs)'% (question, request_time)
    if s == 0:
        'no word found'
        return
    for i in range(len(counts)):
        print "%s.) %s : %.2f (%s fois)"% (i+1, choices[i], counts[i]/s, counts[i])

    return np.argmax(counts)
