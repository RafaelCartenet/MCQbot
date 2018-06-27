#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
from mcqbot import answer
from strategy_tester import test_accuracy
from process_tester import test_process


def bot_test_process():
    data_file= 'data/all.csv'
    test_process(data_file)

def bot_test_accuracy():
    data_file= 'data/all.csv'
    accuracy = test_accuracy(data_file, answer)
    print '\nACCURACY: %2.f%%\n'% (100*accuracy)

if __name__ == '__main__':
    # bot_test_process()
    bot_test_accuracy()



# 68
# 62


# GRAMS COUNT NO unicode handling
# AVERAGE TIME: 1.15s
# ACCURACY: 74%


# SIMPLE COUNT unicode handling.
# 2 pages search
# no delete stopwords for question
# AVERAGE TIME: 1.26s
# ACCURACY: 80%

# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# NO delete stopwords for question
# AVERAGE TIME: 0.96s
# ACCURACY: 85%

# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# WITH delete stopwords for question
# AVERAGE TIME: ?
# ACCURACY: 85%
