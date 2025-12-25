**EXAMPLE DATA**


This directory contains example JSON data for accepted input into the *RunEngine* class. This class is called whenever a *Stateshaper Seed* needs to be created for your data. 


*compound.json*

For 'compound' data ruleset. Takes the terms in the list and creates combinations of them. 

Primary Use: Synthetic Datasets (Quality Assurance, Simulations) 


*random.json*

For 'random' data ruleset. Creates a seemingly "random" set of terms from the data based on the Stateshaper initial_state, constants and mod parameters. 

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

engine.run_engine()
```


