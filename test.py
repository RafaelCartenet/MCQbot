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
    data_file= 'data/12.csv'
    accuracy = test_accuracy(data_file, answer)
    print '\nACCURACY: %2.f%%\n'% (100*accuracy)

if __name__ == '__main__':
    # bot_test_process()
    bot_test_accuracy()

# 2018/06/26 - 141 questions
# GRAMS COUNT NO unicode handling
# 2 pages search
# no delete stopwords for question
# AVERAGE TIME: 1.15s (HOME WIFI)
# ACCURACY: 74%

# 2018/06/26 - 141 questions
# SIMPLE COUNT unicode handling.
# 2 pages search
# no delete stopwords for question
# AVERAGE TIME: 1.26s (HOME WIFI)
# ACCURACY: 80%

# 2018/06/27 - 141 questions
# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# NO delete stopwords for question
# AVERAGE TIME: 0.96s (HOME WIFI)
# ACCURACY: 85%

# 2018/06/27 - 141 questions
# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# WITH delete stopwords for question
# AVERAGE TIME: ? (HOME WIFI)
# ACCURACY: 85%

# 2018/06/27 - 141 questions
# GRAMS COUNT unicode handling (1 3 5)
# 2 pages search
# NO delete stopwords for question
# AVERAGE TIME: 1.64s (OFFICE WIFI)
# ACCURACY: 90%

# 2018/06/27 - 141 questions
# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# NO delete stopwords for question
# AVERAGE TIME: 1.11s (OFFICE WIFI)
# ACCURACY: 90%

# 2018/06/27 - 141 questions
# GRAMS COUNT unicode handling (1 3 10)
# 2 pages search
# NO delete stopwords for question
# AVERAGE TIME: 1.63s (DATA)
# ACCURACY: 88%
