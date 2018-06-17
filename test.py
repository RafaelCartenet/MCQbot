

from mcqbot import answer
from strategy_tester import test_accuracy

data_file= 'data/12.csv'

accuracy = test_accuracy(data_file, answer)

print
print 'ACCURACY: %2.f%%'% (100*accuracy)
print
