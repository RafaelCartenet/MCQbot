# -*- coding: utf-8 -*-

def test_accuracy(data_file, answer_method):
    # Opening the data file
    with open(data_file, 'r') as f:
        questions= f.readlines()

    accuracy= 0.

    for i, question in enumerate(questions):
        question= question.split(';')
        question, choices, right_answer = question[0], question[1:-1], int(question[-1])

        # get the reply using given method
        my_answer= answer_method(question, choices)
        # my_answer= 1

        print '\nQUESTION #%s/%s: %s'% (i, len(questions), question),

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

    return accuracy
