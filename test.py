from pprint import pprint
#
# NLTK
# from nltk.corpus import stopwords
# pprint(stopwords.words("french"))

# assert()




from process_tester import test_process

data_file= 'data/all.csv'
test_process(data_file)

assert()



#
# from mcqbot import answer
# from strategy_tester import test_accuracy
#
# data_file= 'data/all.csv'
#
# accuracy = test_accuracy(data_file, answer)
#
# print
# print 'ACCURACY: %2.f%%'% (100*accuracy)
# print
