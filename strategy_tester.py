# -*- coding: utf-8 -*-

# Rafael Cartenet. 2018

import time

def test_accuracy(data_file, answer_method):
    """ This method is used to evaluate an answer method accuracy. Goes through
    all the question and decide for an answer. Computes as well average running
    time.
    - data_file: the location of a file containing data, see README for format
    - answer_method: function that takes as arguments a question and list of
    choices, and returns the index of the choosen choice.
    """
    # Opening the data file
    with open(data_file, 'r') as f:
        questions= f.readlines()

    # Initializing variables
    accuracy= 0.
    average_time= 0.

    # Iterating through questions
    for i, question in enumerate(questions):

        # Extract question and choices
        question= question.split(';')
        question, choices, right_answer = question[0], question[1:-1], int(question[-1])

        # Display the question and its index
        print '\nQUESTION #%s/%s: %s'% (i+1, len(questions), question)

        # Get the reply using given method
        answer_time= time.time()
        my_answer= answer_method(question, choices)
        answer_time= time.time() - answer_time
        print 'ANSWERING TIME: %.2fs'% (answer_time)

        # Check if answer is correct
        right = False
        if my_answer == right_answer - 1:
            right = True
            # Update accuracy
            accuracy += 1./len(questions)

        print 'RIGHT ANSWER' if right == True else 'WRONG ANSWER'

        # Display all the results and our answer
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

        # Update average time
        average_time += answer_time/len(questions)

    return accuracy, average_time
