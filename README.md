
# Multiple Choice Questions Robot

This is my implementation of a simple bot to answer multiple choice questions (MCQs).
MCQs are questions where the answer is one of the given choices with the question.
For example:

```
Who was the really first president of the United States ?
1.) Abraham Lincoln
2.) Benjamin Franklin
3.) George Washington
```

MCQs are considered as easy for artificial intelligence as the number of possibilities is finite and most of the time really restricted. Most techniques to answer open field questions require semantic analysis in order to understand text and extract the right information at the right place.
We here thus focus on an easier, yet funny, famous NLP problem. We will also discuss at the end the possibilities to use this MCQ bot to reply to "pseudo open field questions".

# Design

The idea is pretty simple, design a function that takes as input a question, and a list of choices, and that returns the index of the choice you believe is the right one.

I came up with a pretty simple idea, by asking myself, how do I normally reply to questions I don't know. Do I reach my shelf to grab a dictionary or do I ask Google ? Easy question.

Indeed, when you ask yourself a question, it is quite likely that Google knows it. My bot thus uses Google to find the answer, in a really simple manner.

```
question;choice1;choice2;...;choiceN;right_answer_index
```


Only french supported for now

```

AMONG ... WHICH ...
AMONG ... WHICH NOT ...

Event:
- During which year
- when's event anniversary

Person/Object


detect if positive or negative

positive -> max occurences
negative -> min occurences


# Results

Accuracy with current code (2018/07/02):

```
AVERAGE TIME: 1.52s
ACCURACY: 88%
```

# Future improvements

TOP PRIORITY:
COUNT FOR 1 gram 2 grams instead of full choice. (or cut)

preprocess question:
- make sure " " aren't first or last character of a word
- overally complexify the .split to words.
- extend mapping
