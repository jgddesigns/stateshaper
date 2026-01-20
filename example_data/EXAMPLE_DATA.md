# *EXAMPLE DATA*


This directory contains example JSON data for accepted input into the *RunEngine* class. This class is called whenever a *Stateshaper Seed* needs to be created for your data. 


<br> <br>


*compound.json*

For 'compound' data ruleset. Takes the terms in the list and creates combinations of them. 


This rule uses the following special values:


**"compound_length": 3 or [3, 4, 7]** 

How many words combined into a string value. Using a list of multiple values will create a variation in the number of combined terms in each output.


**"compound_groups": ["breakfast", "meat", drink]**

Groups to include in the compound. Each generated token will include items only from these included sets. A different token can have different items if there are multiple groups.

***example output: pancakes with sausage and orange juice***


**"compound_terms": ["and", "with"]**

What strings to put in bewteen compounds terms. Examples of potential output include:

sausage and eggs with fruit
oatmeal with berries and yogurt


Primary Use: Synthetic Datasets (Quality Assurance, Simulations) 


<br> <br>


*random.json*

For 'random' data ruleset. Creates a seemingly "random" set of terms from the data based on the Stateshaper initial_state, constants and mod parameters. 


This rule uses the following special values:


**"random_mods": [2, 7]**

Used to test against array positions in order to select the vocab list. 


**"random_constants": [4, 6, 9]**

Used in calculations to create seemingly "random" output while maintaining reproducible determinism. These values will return True if they are the remainder after a 'random_mods' value is tested.


Primary Use: Synthetic Datasets (Procedural Worlds, Code/ID Generation)


<br> <br>


*rating_initial.json*

For 'rating' data ruleset. Creates an output set based on ratings-derived preferences. Only needed during the first run of the engine for each profile. The ratings values can be defineds beforehand using whatever methods deemed necessary. DOES NOT NEED TO BE STORED.

Primary Use: Personalization (Content Feeds, Routine Schedules)


<br> <br>


*rating_derived.json*

The same data from rating_initial, minus the ratings. What is stored on the backend and used for each profile. Base function calls on this data once a profile has been generated (and you used a seed to run the engine).



Example:

```python
# data - the data type from these examples
# token_count (optional, default=10) - the total amount of output values desired  
# constants (optional, default={"a": 3,"b": 5,"c": 7,"d": 11}) - used for morphing calculations. only needss to be modified if specific determinism is needed. 
# mod (optional, default=9973) - used for morphing calculations. only needss to be modified if specific determinism is needed. 
engine = RunEngine(data, token_count)

engine.start_engine()

engine.run_engine()
```


<br> <br>


*tokens.json*

A basic, yet powerful rule. No special data is inputted. Used when you want strictly numeric output. This can be useful for creating a chain of numbers to use as parameters for function logic. 



Example:

```python
# data - the data type from these examples.
# token_count - leave blank, one is generated at a time using this rule.
# initial_state (optional, default=[66, 67, 54, 3, 34]) - the starting number to derive the output from
# constants (optional, default={"a": 3,"b": 5,"c": 7,"d": 11}) - used for morphing calculations. only needss to be modified if specific determinism is needed. 
# mod (optional, default=9973) - used for morphing calculations. only needs to be modified if specific determinism is needed. 
engine = RunEngine(data)

engine.start_engine()

# get first token to use for logic 
token = engine.one_token()

# get the previous token (after one has been generated).
token = engine.reverse_one()
```