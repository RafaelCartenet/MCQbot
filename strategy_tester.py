# -*- coding: utf-8 -*-

def test_accuracy(data_file, answer_method):
    with open(data_file, 'r') as f:
        questions= f.readlines()

    accuracy= 0.

    for question in questions:
        question= question.split(';')
        question, choices, right_answer = question[0], question[1:-1], int(question[-1])

        my_answer= answer_method(question, choices)
        if my_answer == right_answer - 1:
            accuracy += 1

    accuracy /= len(questions)
    return accuracy
