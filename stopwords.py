import nltk

# NLTK
from nltk.corpus import stopwords


frenchstopwords = stopwords.words("french")
frenchstopwords.remove('qui')
frenchstopwords.append('les')
frenchstopwords.append('a')
