# *EXAMPLE DATA*


This directory contains example JSON data for accepted input into the *RunEngine* class. This class is called whenever a *Stateshaper Seed* needs to be created for your data. 



*compound.json*

For 'compound' data ruleset. Takes the terms in the list and creates combinations of them. 


This rule uses the following special values:


**"compound_length": 3** 

How many words combined into a string value.


**"compound_groups": [["breakfast", 1], ["meat", 0]]**

Groups to include in the compound. A 1 in the [1] place of each item indicates every outputted value must include data from this group. A zero indicates an additional group, but one that is not mandatory. In this example, each item in the output list will always be a breakfast group, but not always part of the meat group. Any meat included must be part of the breakfast group.


**"compound_terms": ["and", "with"]**

What strings to put in bewteen compounds terms. Examples of potential output include:

sausage and eggs with fruit
oatmeal with berries and yogurt


Primary Use: Synthetic Datasets (Quality Assurance, Simulations) 




*random.json*

For 'random' data ruleset. Creates a seemingly "random" set of terms from the data based on the Stateshaper initial_state, constants and mod parameters. 


This rule uses the following special values:


**"random_mods": [2, 7]**

Used to test against array positions in order to select the vocab list. 


**"random_constants": [4, 6, 9]**

Used in calculations to create seemingly "random" output while maintaining reproducible determinism. These values will return True if they are the remainder after a 'random_mods' value is tested.


Primary Use: Synthetic Datasets (Procedural Worlds, Code/ID Generation)




*rating.json*

For 'rating' data ruleset. Creates an output set based on ratings-derived preferences. 

Primary Use: Personalization (Content Feeds, Routine Schedules)



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