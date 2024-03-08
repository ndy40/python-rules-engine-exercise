# Description

A simple rules engine in python for evaluating configurable rules for validating input data. 

# How to run? 
1. Minimum Python version required - Python 3.10, this is due to the usage of match pattern matching statements. 
2. Run `pip install -r requirements.txt` to install `tox`. 
3. Run `tox` - This will run the included tests against python version 3.10 to 3.12. 

# Assumptions

## Assumption 1. 
When defining a rule, in the absence of clauses like `and` or `or`, `and` combination is assumed.
Example: `{'temperature': {'is above': 10}, 'age': {'equals': 2}}` will be resolved as `(temperature > 10 and age == 2)`

## Assumption 2.
All rules are currently flat and don't include any nested combination. Example `{'and': {'temperature' {'is above': 10}, 'and': {'age' {'equals': 10}, 'height': {'is less', 5}}}`.

# Improvements
1. Rewrite the engine code to use more of classes than function. 
2. Reduce nested if statements. 
3. Find an alternative way to express rules possibly as text and write a parser to translate a text based rule to executable python code. 


