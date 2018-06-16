

from mcqbot import answer_v1
from strategy_tester import test_accuracy

data_file= 'data/train.csv'

accuracy = test_accuracy(data_file, answer_v1)

print
print 'ACCURACY: %2.f%%'% (100*accuracy)
print
