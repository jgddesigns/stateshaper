**QUICK START GUIDE**


The Stateshaper Engine will give you a list/array of deterministic events or variables to use in your logic. 

For continuous use, the engine can be called in a loop using the *run_engine* function. For one time, call it once with a specific *token_count* parameter.

To create the same output again, *start_engine* needs to be called once more.


1. Make sure your data is in one of the formats listed in the *"example_data"* directory. 


2. Initialize a *RunEngine* class 

```python
from .run import RunEngine 

# data (REQUIRED) - the input data. must be in a format listed in the 'example_data' directory
# token_count (default=10) - The desired size of the list containing your input terms.
# constants (optional) - Only change this for custom morphing equations.
# mod (optional) - Only change this for custom morphhing equations

#BASIC
engine = RunEngine(data=your_data, token_count=needed_tokens)

#CUSTOM
engine = RunEngine(data=your_data, token_count=needed_tokens, constants=optional_custom_logic, mod=more_optional_logic)

engine.start_engine()
```


3. Call the *run_engine* method.

```python
engine.run_engine()

# OUTPUT    
#
# ["your", "input", "values", "are", "returned", "based", "on", "chosen", "stateshaper", "rules"]
```


Whatever the decided use is, this tool can achieve it using almost no stored memory. 

Unlimited sequences of data can be re-created from a small seed, including fully personalized user profiles. 

Privacy is achieved through obfuscation. The data can't be interpreted without using the seed as a key.