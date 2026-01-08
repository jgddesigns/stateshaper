# *Stateshaper*

**Compress data and generate content using small seeds.**


The origin of this idea started with the 'Infinite Map Concept' I created in early 2025. The core logic starts with the idea of using a static length array of numbers which has values that change based on a mathematic function. The function uses a modulus operator to keep the array within a fixed range of values. Because of this, continuing to run the engine will produce an unbound chain of deterministic output. 

This idea was improved upon with some help from ChatGPT, and has become *Stateshaper*.

The primary benefits of *Stateshaper* are compression, enhanced privacy, and memorization. 

As far as compression is concerned, using this tool can reduce data sizes by over 90%. This saves money on both database storage and bandwidth. This is because large amounts of memorized data can be generated from the small, JSON-formatted seed the engine produces during its initial run. 

Compressing this data also allows for privacy, where the data contained in a seed it can't be extracted without knowing specific seed parameters. For applications, this can be stored in environment variables the same way that access keys can.


Recommended Uses Include:

- Content Feeds
- Routine Planner
- Personalized Suggestions
- QA Stress Testing
- Procedural World Generation


This repository contains code written in Python, with other langauges scheduled to be available soon. 

Tests have been created to demonstrate *Stateshaper* engine functionality.

These can be found in the src/main/tests directory.

Additonally, two demonstrations are live online:

*Targeted Ads Compression Demo*

https://stateshaper-ads.vercel.app

Demonstrates the engine's ability to generate data based on personalization. Ads shown are based on user preference ratings and can be adjust in the app. The data needed to recreate the entire profile is condensed into a ~50-250 byte JSON string. 


*Lesson Plans Demo*

https://stateshaper-lessons.vercel.app

An example of a personalized learning plan based on a student's performance. Condenses the entire profile into a small seed. 


*Tiny State Compression*

https://tiny-state.streamlit.app

An interactive tool that shows how a *Stateshaper* seee can be compressed even further in ~8 bytes. A seed can be compressed, extracted and re-compressed continually and maintain its original values. 

---



## Features

- **Deterministic** – same seed → same output on any machine.
- **Lightweight** – core state is just a handful of integers (< 1 KB).
- **No training** – no datasets, no GPUs, no model weights.
- **Semantic output** – not just random noise; tokens can represent text, events, or structures.
- **Reproducible** – perfect for QA, research, and simulation replays.
- **Offline-friendly** – runs on laptops, servers, and small embedded devices.



---



## Quick Start

### Installation

Clone this repository:

```bash
git clone https://github.com/jgddesigns/stateshaper.git
cd stateshaper
```



**Make sure your data is in one of the formats listed in the *"example_data"* directory. The output that is generated depends on the values contained in this dataset. The data types are based on the following rules:**

***If needed, use the *FormatData* class in the nested *'format_data'* directory.***

Instructions: [`Formatting Data for Input`](example_data/format_data/FORMAT_DATA.md)



*Compound* - A collection of items that include a specified group. Only items from the defined groups will be part of the final output.

Example: [`Compound Dataset`](example_data/compound.json)


*Rating* - Creates a sense of personalization for the output. The output is initially created based on a ratings preference. Afterward, the output is derived from the current included items and adjusted based on whatever parameters are decided upon (such as user input). The *'derived'* dataset is all that needs to be saved on the backend, and does not include a *'rating'* key. It can be used for all profiles in an application.

Example: [`Initial Rating Dataset`](example_data/rating_initial.json), [`Derived Rating Dataset`](example_data/rating_derived.json) 


*Random* - A seemingly random array of the included items is generated. Only one item from the master dataset is included per engine step.

Example: [`Random Dataset`](src/main/connector/random.json)







**Initialize a *RunEngine* class:**

```python
# data (REQUIRED) - the input data. must be in a format listed in the 'example_data' directory
# seed (optional) - required to recreate a previous run of the engine. it is created after the first run of the engine. when used, no other parameters other than token count need to be specified. if no custom parameters are set, only the "v" key with state format data needs to be included. (ex. seed={"v": ["ABC12345", "BVCH457SZ"]})
# token_count (default=10) - The desired size of the list containing your input terms.
# constants (optional) - Only change this for custom morphing equations.
# mod (optional) - Only change this for custom morphhing equations

from stateshaper import RunEngine

# BASIC (first run)
engine = RunEngine(data=your_data, token_count=needed_tokens)

# RE-CREATE PREVIOUS OUTPUT
engine = RunEngine(data=your_data, seed=created_seed, token_count=needed_tokens)

# CUSTOM
engine = RunEngine(data=your_data, seed=created_seed, token_count=needed_tokens, constants=optional_custom_logic, mod=more_optional_logic)

engine.start_engine()
```



**Call the *run_engine* method:**

```python
engine.run_engine()

# OUTPUT    
#
# ["your", "input", "values", "are", "returned", "based", "on", "chosen", "stateshaper", "rules"]
```


For continuous use, the engine can be called in a loop using the *run_engine* function. For one time, call it once with a specific *token_count* parameter.

To create the same output again, *start_engine* needs to be called once more.

---



## Core Logic Example
### Details of the Stateshaper Main Class

*Stateshaper* uses an evolving array of numbers that can be tokenized to call events or variables. 

This section shows examples of the main classes included in the engine. **They are not meant to be ran individually**.


```python
from main.core import Stateshaper
from main.plugins.PluginData import PluginData

# Small numeric seed (arbitrary integers unless otherwise needed). These values are the starting array to base the math on. Their state is what the vocab data is called from from. The array length stays consistant as the numbers change. 
#
state = [12, 7, 4, 19, 3, 11, 5, 8, 2]

# Tokens that are generated during each iteration of the program. For instance, this set of events can be used to generate sprites in a video game map. 
#
vocab = ["plant", "office building", "pedestrian", "tree", "pavement"...] 
#
# other examples include:
# vocab = ["string1", "string2", "string3"...]
# vocab = [event1, event2, event3...]
#  
# Class instantiation. The parameters are the only values that need to be stored other than your app's custom plugin file. In the most minimal cases, only the vocabulary is needed to be stored.
engine = Stateshaper(
    state=state,
    vocab=vocab,
    constants={"a": 3, "b": 5, "c": 7, "d": 11},
    mod=9973,
)

# Generate 20 tokens. 
tokens = [engine.next_token() for _ in range(20)]
# Example Output : ["tree", "tree", "pedestrian", "tree", "office building", "pedestrian", "pavement"....]

# Use the tokens to call events.
# The first parameter, i is the type of sprite to draw.
# The second parameter is a number from the state array (1 - mod, 9973). This can be used in the drawing function to add variations like color, size and position. 
events = [i for plugin.draw(i, state[tokens.index(i)]) in tokens]



```


# Connector Class

The *Connector* class can take your data and process it to be ready for compression into seed format.  

For more ino, see the [`CONNECTOR`](src/main/connector/CONNECTOR.md) documentation.  



---



# TinyState Class

Aside from the plugin file (which can be a template that does not include specific numbers), relevant data such as the event map and ratings can be condensed into *Tiny State* and/or *Raw State* format. Example:

**Tiny State: ABC-12345**

**Raw State: QV589JX4**

These values can be encoded and decoded in the *TinyState* class within the 'tools' directory. The main data map is represented as a long string of numbers. These numbers stand for positions in the map and are encoded into *Tiny State* format. A subset of numbers from the vocab used in the engine is also kept and encoded into *Raw State* format.


```python 
class TinyState:

   # return: Coded dataset. 
   # return[0]: Tiny State seed. Reperesents the compressed values for the master data set.
   # return[1]: Raw State seed. Represents the subset of personalized values chosen for the specific instance.
   def get_seed(data):
      # Encode logic
      # This is the value that will be kept in the database. It is where most of the compression happens. 
      return ["ABC-12345", "QV589JX4"]

   # return: personalized events for the specific user/instance.
   def rebuild_data(master_seed, subset_seed):
      # Decode logic.
      # Numbers values from the seeds stand for key/value pairs from the master dataset and are kept in groups of four in data sets length 100 or less. If more length is needed the group size can be increased.
      #
      # Example: 0214 stands for key #3, value #15 
      return ["event1", "event2", "event3"...]
```

 
For a given user, all that will be needed to be stored for the above example is:

["user-1234", ["abc-12345", QV589JX4]]

From that, all other content can be generated during run time, and be personalized to each user. 

The ratings can be modified as needed, then re-encoded as a different seed. 

For some uses, a longer seed may be required. Sometimes this can be because a custom initial state, mod or constants are  required. Also if a very large amount of data causes the *Tiny State* seed to need additional characters. 

In total, there are four types of data used in *Stateshaper*. They are really just strings, dicts and lists in a certain format. The specific formats are as follows:


Full State:
```python

seed = {"user_id": "johnq1234", "signature": [3404,832,2194, 6734,105],"series_seed": 3404,"mod": 9973,"constants": {"a": 3,"b": 5,"c": 7,"d": 11}}

# ~225 bytes

```


Short State:
```python

seed = ["user_176551",[3404,832,2194,6734,105],["ABC12345", "567yQ90T34"]]

# ~65 bytes

```


Tiny State
```python

seed = "ABC12345"

# ~8 bytes

```

Raw State
```python

seed = "567yQ90T34"

# ~10 bytes

```


The format needed will vary depending on the needs for each application. For applications needing only continuous, random data Tiny or Raw format may be all that is needed. For those that require more complex, personalized data, *Full State* may be needed. A combination of any of these can be used, as long as the required 'vocab' parameter is passed into the engine.


For more info, see the [`TINY_STATE`](src/main/tools/tiny_state/TINY_STATE.md) documentation.



---



## How It Works 

The 'seed' array, 'constants' and 'mod' value are used for calculations during each iteration. The array numbers during that iteration are used to call tokens from the list of values defined in the 'vocab' parameter. This can be seemingly random if needed, or designed to occur in a specific sequence. 

For basic use, no plugin is required. Only an array of the tokens (variables or functions) is needed. If no particular order is needed (such as generating data to stress test a system for QA, or cooking app that suggests a random recipe) this may be all that is needed.

For more specialized designs, a custom plugin file can be written. This will be used along with *Stateshaper* *'Connector'* class to define specific rules for the tokens included in 'vocab' list. This can be based on developer needs and can be based on attributes, sequence or frequency the tokens are called if needed.

**Considerations for Designing Custom Plugins**

1. Define a Token List 
Them 'vocab' parameter. This can be an array of any type of values, including functions. A custom plugin file can be written if needed.

2. Are Custom 'seed', 'constants' or 'mod' Values  Needed?
If specific deterministic output is needed, these values ca be adjusted to fit with the morph equation.

3. Is a Custom Morph Rule Needed?
The math done to change the array values can also be altered. This can allow for further customization of the deterministic array.

4. Call *Stateshaper* Class Object and Pass the Created Parameters. 

5. Generate the Ouput
Create as many tokens as needed with *Stateshaper*().generate_token(x) method. This can be called all at once or during a loop.

6. Modify the Stream if Needed 
The data can be changed based on input such as user behavior or duration. The main class variables can be assigned new values in real time, or a new instance of the class can be created. 



---



## Running Tests

Tests can be ran using the *Tests* class.

These tests demonstrate *Stateshaper's* ability to generate data against popular existing algorithms. 

Areas of focus include determinism, reversibility, personalization, direct indexing, semantic flow and compression.

For more info, see the [`TESTS`](src/main/tests/TESTS.md) documentation.



--- 



## Use Cases (Expanded)

### Personalization Without Storing User Data

Personal Ads or News
Fitness Routine
Smart Home Scheduling
Student Test Sets/Lesson Plans

Assign each user a seed and derive their long-term content pattern from it, without storing
behavioral data or personally identifiable information. The output evolves over time based on input such as user interaction.


### Synthetic Data 

Video Game Simulations
QA System Testing
Fintech Data
Experimental Values

Generate large, reproducible datasets from a single small seed. This avoids privacy issues and reduces cost compared to collecting real-world data. Relevant data can be continually created and called within an application.


### Structures

Inventory 
Application Content
Bookkeeping
Statistical Records

Condense large amounts of data into smaller objects. Generate it in real-time based on a set of defined terms/rules. 



---



## Project Structure

```text
stateshaper/
├── api
|     ├── run_api.py
|     ├── API.md
├── example_data
|     └── format_data/
|        ├── FormatData.py
|        ├── FORMAT_DATA.md
|     ├── compound.json
|     ├── random.json
|     ├── rating_derived.json
|     ├── rating_initial.json
|     ├── EXAMPLE_DATA.md
├── src/
│   └── main/
|        └── connector/
|              ├── Connector.py
|              ├── Modify.py
|              ├── Vocab.py
|              ├── CONNECTOR.md
|        └── demos/
|              └── ads
|                    ├── ad_list.py
|                    ├── Ads.py
|              └── fintech
|                    ├── coming soon
|              └── infinite_map
|                    ├── coming soon
|              └── inventory
|                    ├── coming soon
|              └── lesson_plan
|                    ├── lessons_list.py
|                    ├── LessonPlan.py
|              └── meal_plan
|                    ├── coming soon
|              └── smart_home
|                    ├── coming soon
|              ├── DEMOS.md
|        └── plugins/
|              └── compression
|                    ├── coming soon
|              └── personalization
|                    ├── coming soon
|              └── procedural
|                    ├── coming soon
|              └── structured
|                    ├── coming soon
|              └── synthetic
|                    ├── coming soon
|              ├── PLUGINS.md
|        └── tests/
|              └── ca
|                    ├── coming soon
|              └── markov
|                    ├── Markov.py
|              └── ml
|                    ├── coming soon
|              └── prng
|                    ├── coming soon
|              └── probalistic
|                    ├── coming soon
|              ├── TESTS.md
|              ├── Tests.py
|        └── tools/
|              └── derive_vocab
|                 ├── DeriveVocab.py
|                 ├── DERIVE_VOCAB.md
|              └── tiny_state
|                 ├── TinyState.py
|                 ├── TINY_STATE.md
|              ├── Morph.py
|              ├── TokenMap.py
|              ├── TOOLS.md              
│       ├── core.py
│       ├── stateshaper.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── QUICK_START.md
├── README.md
├── setup.py


```



## Contributing

Contributions, ideas, and experiments are welcome!

See [`CONTRIBUTING`](CONTRIBUTING.md) instructions if you are interested in creating a custom plugin (or anything else).



---



## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.

If you use this in research, products, or experiments, a mention or citation of the
"Stateshaper" is appreciated.
