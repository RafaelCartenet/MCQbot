
from strategy_tester import test_accuracy
from mcqbot import answer

def bot_test_accuracy():
    data_file= 'data/data_french.csv'
    accuracy, average_time = test_accuracy(data_file, answer)
    print '\nAVERAGE TIME: %.2fs'% average_time
    print '\nACCURACY: %2.f%%\n'% (100*accuracy)

if __name__ == '__main__':
    bot_test_accuracy()
