# *FORMATTING DATA FOR INPUT



Takes your data and formats it for input into the *Stateshaper* engine.



## **Instructions:**


### *COMPOUND* RULESET 

Call the *'build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.
build_data("compound", 5)

# sample output
# chocolate, lemon, orange, hazelnut, pecan
```


Call the *'add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule as a paramter, the item as another and the groups the item belongs to.
add_row("compound", "chocolate", ["candy", "cake", "pie", "chocolate"])

add_row("compound", "lemon", ["candy", "pie", "fruit", "juice"])

add_row("compound", "orange", ["candy", "fruit", "juice"])
```


Call the *'add_group'* function to specify which groups you want the dataset to output.

```python
# pass a list as a parameter that includes the group name and 1 for if it is required or 0 if included but not required

# every item outputted will be a type of candy
add_group("candy", 1)

# some of the candy items will be chocolate. all of the chocolate items will be candy.
add_group("chocolate", 0)

# chocolate items will be candy or pie, but not cake.
add_group("pie", 1)
```


Call the *'add_term'* function to specify which terms you want to be used to combine dataset items.

```python
# pass the term as a string
add_term("and")

# sample output
# chocolate candy and chocolate pie
```


Call the *'add_compound_length'* function to specify how many items you want compounded together for the final output. If you want variation, pass it as a list. The default value is 2.

```python
add_compound_length(3)

# sample item created from dataset
# chocolate pie and orange candy as well as hazelnut candy
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine
get_data()
```




### *RANDOM* RULESET 

Call the *'build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.
build_data("random", 5)

# sample vocab input derived from dataset
# macaroni and cheese, frozen yogurt, chicken alfredo, tuna sandwich, pad thai
```


Call the *'add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule data item as parameters 
add_row("random", "macaroni and cheese")

add_row("random", "chicken pot pie")

add_row("random", "frozen yogurt")
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine
get_data()
```




### *RATING* RULESET 

Call the *'build_data'* function to generate a data template. 

```python
# pass the data ruleset and length of items included from the data as a parameter. default amount is 3 if length is not passed.
build_data("rating", 5)

# sample vocab input derived from dataset
# sports, action, fantasy, puzzle, fps
```


Call the *'add_row'* function for each item intended to be in the final dataset.

```python
# pass the rule and items as the parameter to define the row
add_row("rating", "baseball.png", ["baseball", "basketball", "football"], "sports")

add_row("rating", "boggle.png", ["scrabble", "jenga"], "puzzle")

add_row("rating", "wow.png", ["final fantasy", "fallout", "overwatch"], "mmorpg")
```


Call the *'add_rating'* function for each item intended to be in the final dataset.

```python
# use the item as one parameter and its preference rating in another. obtain the ratings however you see fit. 
add_rating("sports", 75)

add_rating("puzzle", 53)

add_rating("mmorpg", 95)
```


Obtain the final dataset.
```python
# retrieves data in the format needed for input into the stateshaper engine.
# this data is only for the initial dataset. after you run the engine once with this data, get the new master dataset from the RunEngine class and use it going forward. for more instructions, see the QUICK_START or README documentation. 
get_data()
```