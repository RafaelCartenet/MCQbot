
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

MCQs are considered as quite easy in the domain of artificial intelligence as the number of possibilities is finite and most of the time really restricted. Most techniques to answer open field questions however, require semantic analysis in order to understand some text and extract the right information at the right place.
We here thus focus on an easier, yet funny, famous NLP problem. We will also discuss at the end the possibilities to use this MCQ bot to reply to "pseudo open field" questions.

# Design

The idea is pretty simple, design a function that takes as input a question, and a list of choices (number of choices is not fixed), and that returns the index of the choice you believe is the right one.

I came up with a pretty simple idea, by asking myself, how do I normally reply to questions I don't know. Do I reach my shelf to grab a dictionary or do I ask Google ? Easy question.

Indeed, when you ask yourself a question, it is quite likely that Google knows it. My bot thus uses Google to find the answer, in a really simple manner.

# Data

I created a simple dataset, that contains for now only french samples. The format is pretty simple:

```
question;choice1;choice2;...;choiceN;right_answer_index
```

That means for the above example we would have:
```
Who was the really first president of the United States ?;Abraham Lincoln;Benjamin Franklin;George Washington;3
```

Data can be found in the data subfile, that contains only for know a little french dataset that I have been using.
**Feel free to use it, increase it, or create new ones and share them with me.**

# Installation

This project has been developped in python **2.7**, the good ol' verision.
Requirements can be found in the file requirements.txt, install them with pip:
```
pip install -r requirements.txt
```

nltk==3.2.1
numpy==1.11.1
protobuf==3.6.0
Google-Search-API==1.1.13

# Results

I added a simple function call **test_accuracy**, that you can find in **strategy_tester.py** in order to test a MCQ bot strategy.
I used this function to evaluate my bot after each upgrades in order to measure improvements.
To evaluate my bot, or your own, you can just modify the file **run_me.py**:

```py
from strategy_tester import test_accuracy
from mcqbot import answer

def bot_test_accuracy():
    data_file= 'data/data_french.csv'
    accuracy, average_time = test_accuracy(data_file, answer)
    print '\nAVERAGE TIME: %.2fs'% average_time
    print '\nACCURACY: %2.f%%\n'% (100*accuracy)

if __name__ == '__main__':
    bot_test_accuracy()
```


**(2018/07/02)** My accuracy with current best strategy:

```
ACCURACY: 88%
AVERAGE TIME: 1.52s
```

Interestingly enough, as results depend on google searchs, and that the latter is
depending on a bunch of stuff including the cookies and everything, accuracy varies regarding the place you are (the wifi or data provider you are using),
the time of the day etc. It is thus pretty tough to agree on a single value for accuracy.

# Future improvements
