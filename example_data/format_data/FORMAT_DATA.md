# FORMATTING DATA FOR INPUT



Takes your data and formats it for input into the *Stateshaper* engine. 



## **Instructions:**


### *COMPOUND* RULESET 

Call the *'format_data.build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.

format_data.build_data("compound", 5)

# sample output
# chocolate, lemon, orange, hazelnut, pecan
```


Call the *'format_data.add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule as a paramter, the item as another and the groups the item belongs to.

format_data.add_row("compound", "chocolate", ["candy", "cake", "pie", "chocolate"])

format_data.add_row("compound", "lemon", ["candy", "pie", "fruit", "juice"])

format_data.add_row("compound", "orange", ["candy", "fruit", "juice"])
```


Call the *'format_data.add_group'* function to specify which groups you want the dataset to output.

```python
# add lists of groups that will be grouped together. terms featuring these groups will be outputted in various combinations. there can be multiple groups, but each specific output will only include items from one particular group.

# this will create combinations of items from candy and chocolate groups.
format_data.add_group(["candy", "chocolate"])

# example output
# caramels, chocolate covered almonds and fudge

# another collection of groups
format_data.add_group(["candy", "flowers", "card"])

# example output
# buttscotch discs and lifesavers with roses, carnations and a thank you note

# an item from the compound dataset is formatted as follows:
#
# {
#    "data": "cake",
#    "groups": ["dessert", "sweet"]
# }
```


Call the *'format_data.add_term'* function to specify which terms you want to be used to combine dataset items.

```python
# pass the term as a string:

format_data.add_term("and")

# sample output
# chocolate candy and chocolate pie
```


Call the *'format_data.add_compound_length'* function to specify how many items you want compounded together for the final output. If you want variation, pass it as a list. The default value is 2.

```python
format_data.add_compound_length(3) # can be a list of integers for varied output lengths ex. [2, 3, 5]

# sample item created from dataset:
# chocolate pie and orange candy as well as hazelnut candy
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine.

format_data.get_data()
```




### *RANDOM* RULESET 

Call the *'format_data.build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.

format_data.build_data("random", 5)

# sample vocab input derived from dataset:
# macaroni and cheese, frozen yogurt, chicken alfredo, tuna sandwich, pad thai
```


Call the *'format_data.add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule data item as parameters.

format_data.add_row("random", "macaroni and cheese")

format_data.add_row("random", "chicken pot pie")

format_data.add_row("random", "frozen yogurt")
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine.

format_data.get_data()
```




### *RATING* RULESET 

Call the *'format_data.build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.

format_data.build_data("rating", 5)

# sample vocab input derived from dataset
# sports, action, fantasy, puzzle, fps
```


Call the *'format_data.add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule, item, attributes, and main attribute as parameters for the row.

format_data.add_row("rating", "baseball.png", ["baseball", "basketball", "football"], "sports")

format_data.add_row("rating", "boggle.png", ["scrabble", "jenga"], "puzzle")

format_data.add_row("rating", "wow.png", ["final fantasy", "fallout", "overwatch"], "mmorpg")
```


Call the *'format_data.add_rating'* function for each item intended to be in the final dataset.

```python
# use the item as one parameter and its preference rating in another. obtain the ratings however you see fit. 

format_data.add_rating("sports", 75)

format_data.add_rating("puzzle", 53)

format_data.add_rating("mmorpg", 95)
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine.
# this data is only for the initial dataset. after you run the engine once with this data, get the new master dataset from the RunEngine class and use it going forward. for more instructions, see the QUICK_START or README documentation. 

format_data.get_data()
```