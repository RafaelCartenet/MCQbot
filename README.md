

# Multiple Choice Questions Robot

Questions format:

```
question;choice1;choice2;...;choiceN;right_answer_index
```


Only french supported for now

Example:

```
Quels héros de bande dessinée sont les maîtres du chien Kador ?;Tom-Tom et Nana;Les Dalton;Les Bidochon;3
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


# Future improvements

TOP PRIORITY:
COUNT FOR 1 gram 2 grams instead of full choice. (or cut)

preprocess question:
- make sure " " aren't first or last character of a word
- overally complexify the .split to words.
- extend mapping
