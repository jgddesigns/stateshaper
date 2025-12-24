**HOW TO USE THE PLUGIN CONNECTOR**


---


1. Make sure you have your events and corresponding preference ratings mapped in the proper format. Example:

```python


{
    "input": [
        {
            "data": "grilled chicken salad",
            "rating": 14

            # OPTIONAL (used when compound rule is set)
            "groups": ["sandwich", "meat", "lunch"]
        },
        {
            "data": "spaghetti bolognese",
            "rating": 14

            # OPTIONAL
            "groups": ["pasta", "italian"]
        },
        {
            "data": "vegetable stir fry",
            "rating": 14
        },
        {
            "data": "cheeseburger",
            "rating": 45
        },
        {
            "data": "pepperoni pizza",
            "rating": 88
        },
        {
            "data": "fish tacos",
            "rating": 35
        },
        {
            "data": "beef burrito",
            "rating": 75
        },
        {
            "data": "chicken alfredo",
            "rating": 65
        },
        {
            "data": "lentil soup",
            "rating": 25
        },
        {
            "data": "bbq ribs",
            "rating": 92
        },
        {
            "data": "avocado toast",
            "rating": 3
        },
        {
            "data": "shrimp fried rice",
            "rating": 55
        },
        {
            "data": "pancake breakfast",
            "rating": 77
        }
    ],

    "rules": "rating",
    "length": 10,


    # OPTIONAL KEYS

    # when the compound rule is chosen, defines how many terms go together for each output
    # default value is 3 (if compound rule is chosen and this key is not included in the input dataset)
    "compound_length": 3, 

    # the base value used in equations that define how vocab values are compounded
    # default value is 7 (if compound rule is chosen and this key is not included in the input dataset)
    "compound_modifier": 7,

    # if a group key is included in the items list, can be used to limit what values are grouped together
    # the following will group only these values together in the output
    # example outputs:
    #
    # vocab = ["meatball sandwich", "bratwurst", "sausage sandwich", "hot dog", "cornbread", "fries", "chili", "chips", "salad", "chicken # salad", "almond", "walnuts"]
    #
    # meatball sandwich with chips
    # bratwurst and fries
    #
    # default value is None, meaning anything in the vocab list can be compounded
    # first values is a key in the groups value that is part of each item. second value indicates if the group is mandatory for each compound. 1 indicates mandatory, 0 indicates optional. 
    "compound_groups": [["meat", 0], ["lunch", 1], ["side", 0]],

    # the terms used in between compound words. if there are more words than compound length, they will be randomly used. otherwise they will occur in the order they are in the list for each final term that is outputted. 
    # default value is " " if not set. 
    "compound_terms": ["and", "with", "including", "plus", ","]

    # used when the random rule is set. the base value used in equations to randomize the input
    # default value is 21 (if random rule is chosen and this key is not included in the input dataset)
    "modifier" : 21
}


```

input:
    data: Can be any data type. For instance, a string, number or function. This is what will be called as the *Stateshaper* Engine is running. 
    rating: This is the preference rating for each item in the input list. A higher rating will be added with priority. 

rules:
    In this case the rule is always "rating" due to the data being used for personalization. 

    Other rules include:

        Random - Use no rating system for personalization. Data list in the vocab parameter is outputted in no particular order, but is memorized. Choosing this rule also randomizes the initial state, constant, and modulus values. This is based on a modifier value that can be included in the dataset, which can be chosen and defaults at 21.  

        Compound - 

        Token - 

length:
    The length of the vocab list to be passed into the engine. This is what will be called as the engine runs. 




2. Call *Connector* class, passing the above data object as a parameter. 

3. To get the seed to pass into the engine, call the *Connector* function, *start_connect*. 


---


**Modification**


These functions are part of the *Connector* class. When used, the ratings associated with events can be adjusted. This has a direct effect on the personalization of the output. In other words, the events with the highest ratings will occur more frequently in the stream created by the engine. If a length is set in the main data object, only the values with the highest ratings will be included in the engine vocab. 


```python
def set_value(self, key, rating):
    self.modify.modify(key, rating)
```

*Sets the value of a specific item in the data input object.*

```python
def adjust_value(self, key, adjust):
    self.modify.adjust(key, adjust)
```
    
*Adds or subtracts the rating for a specific item.*

```python
# REQUIRED
def alter_stream(self):
    self.data["input"] = self.modify.export()
    self.start_connect()
```

*After calling ***set_value*** or ***adjust_value***, returns the seed used in the Stateshaper engine. If the function is not called, the stream will not be modified.*