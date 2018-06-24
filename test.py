#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
from mcqbot import answer
from strategy_tester import test_accuracy
from process_tester import test_process


def bot_test_process():
    data_file= 'data/12.csv'
    test_process(data_file)

def bot_test_accuracy():
    data_file= 'data/12.csv'
    accuracy = test_accuracy(data_file, answer)
    print '\nACCURACY: %2.f%%\n'% (100*accuracy)

if __name__ == '__main__':
    # bot_test_process()
    bot_test_accuracy()
