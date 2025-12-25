**EASY INSTRUCTIONS FOR USE**


The Stateshaper Engine will give you a list/array of deterministic events or variables to use in your logic. 

For continuous use, the engine can be called in a loop. For one time, call it once with a specific token_count parameter.


1. Make sure your data is in one of the formats listed in the *"example_data"* directory. 


2. Initialize a *RunEngine* class 

```python
# data (REQUIRED) - the input data. must be in a format listed in the 'example_data' directory
# token_count (default=10) - The desired size of the list containing your input terms.
# constants (optional) - Only change this for custom morphing equations.
# mod (optional) - Only change this for custom morphhing equations

#BASIC
engine = RunEngine(data=your_data, token_count=needed_tokens)

#CUSTOM
engine = RunEngine(data=your_data, token_count=needed_tokens, constants=optional_custom_logic, mod=more_optional_logic)
```


3. Call the *run_engine* method.

```python
engine.run_engine()

# OUTPUT    
#
# ["your", "input", "values", "are", "returned", "based", "on", "chosen", "stateshaper", "rules"]
```