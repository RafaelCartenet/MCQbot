# -*- coding: utf-8 -*-

import time

def test_accuracy(data_file, answer_method):
    # Opening the data file
    with open(data_file, 'r') as f:
        questions= f.readlines()

    accuracy= 0.
    average_time= 0.

    for i, question in enumerate(questions):
        question= question.split(';')
        question, choices, right_answer = question[0], question[1:-1], int(question[-1])

        print '\nQUESTION #%s/%s: %s'% (i+1, len(questions), question)

        # get the reply using given method
        answer_time= time.time()
        my_answer= answer_method(question, choices)
        answer_time= time.time() - answer_time
        # my_answer= 1

        print 'ANSWERING TIME: %.2fs'% (answer_time)

        right = False
        if my_answer == right_answer - 1:
            right = True
            accuracy += 1./len(questions)

        print 'RIGHT ANSWER' if right == True else 'WRONG ANSWER'

        for i, choice in enumerate(choices):
            if i == right_answer - 1:
                print 'o ',
            else:
                print 'x ',
            print choice,
            if i == my_answer:
                print '<'
            else:
                print ' '

        average_time += answer_time/len(questions)

    print '\n\nAVERAGE TIME: %.2fs'% average_time
    return accuracy
