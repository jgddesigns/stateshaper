# *Stateshaper*

**Compress data and generate content using small seeds.**

*Clean up database tables by generating data in real-time within your app.*


The origin of this idea started with the 'Infinite Map Concept' I created in early 2025. The core logic starts with the idea of using a static length array of numbers which has values that change based on a mathematic function. The function uses a modulus operator to keep the array within a fixed range of values. Because of this, continuing to run the engine will produce an unbound chain of deterministic output. 

Using a custom plugin file, events can be mapped to the array by tokenizing its values. The engine allows for the events be called for as long as needed. The events can include many types of data including strings, links, images and functions. Due to the nature of the algorithm, the mapped events can be condensed and extracted as *Stateshaper* runs.

This idea was improved upon with some help from ChatGPT, and has become the Morphic Semantic Engine.

Recommended Uses Include:

- Synthetic data generation
- Deterministic simulations
- Procedural text & lore
- Privacy-safe personalization
- Embedded / offline generative behavior

This repository contains a reference implementation in Python, example scripts, and documentation.


Tests have been created to demonstrate *Stateshaper* engine functionality.

These can be found in the src/main/tests directory.


Additonally, two demonstrations are live online:


*Targeted Ads Compression Demo*

https://stateshaper-ads.vercel.app


*Tiny State Compression*

https://tiny-state.streamlit.app


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


The *Stateshaper* class needs to be called as follows...


---



## Basic Example

*Stateshaper* uses an evolving array of numbers that can be tokenized to call events or variables. 


```python
from main.core import *Stateshaper*
from main.plugin import PluginData

# Small numeric seed (arbitrary integers unless otherwise needed). These values are the starting array to base the math on. Their state is what the vocab data is called from from. The array length stays consistant as the numbers change. 
#
seed = [12, 7, 4, 19, 3, 11, 5, 8, 2]

# Tokens that are generated during each iteration of the program. For instance, this set of numbers is chosen based on a rating system in the plugin file. When tokenized, they can call desired output from the plugin. They can be modified as the engine runs if the output needs to be changed. This allows for personalization and can be based off of variables such as user behavior. 
#
vocab = [1, 2, 3, 6, 7, 9] 
#
# other examples include:
# vocab = ["string1", "string2", "string3"...]
# vocab = [event1, event2, event3...]
#  
# Class instantiation. The parameters are the only values that need to be stored other than your app's custom plugin file. In the most minimal cases, only the vocabulary is needed to be stored.
engine = *Stateshaper*(
    seed=seed,
    vocab=vocab,
    constants={"a": 3, "b": 5, "c": 7, "d": 11},
    mod=9973,
)

# Generate 20 tokens. 
tokens = [engine.next_token() for _ in range(20)]
print(" ".join(tokens))
# [3, 6, 1, 3, 2, 7, 1, 2, 9....]

# Use the tokens to call events. See PluginData class below.
events = [i for plugin.get_event(i) in tokens]

```


# Connector

The *Connector* class can take your data and compress it into seed format, making it usable in the *Stateshaper* engine. Right now this is mostly for personalization purposes, but may be modified going forward. 

For more ino, see the [`src/main/connector/CONNECTOR.md`](CONNECTOR.md) file.  



---



# Data Formats

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


The format needed will vary depending on the needs for each application. For applications needing only continuous, random data Tiny or Raw format may be all that is needed. For those that require more complex, personalized data, Full State may be needed. A combination of any of these can be used, as long as the required 'vocab' parameter is passed into the engine.


For more info, see the [`src/main/tools/tiny_state/TINY_STATE.md`](TINY_STATE.md) file.


---



## How It Works 

The 'seed' array, 'constants' and 'mod' value are used for calculations during each iteration. The array numbers during that iteration are used to call tokens from the list of values defined in the 'vocab' parameter. This can be seemingly random if needed, or designed to occur in a specific sequence. 

For basic use, no plugin is required. Only an array of the tokens (variables or functions) is needed. If no particular order is needed (such as generating data to stress test a system for QA, or cooking app that suggests a random recipe) this may be all that is needed.

For more specialized designs, a custom plugin file can be written. This will be used along with *Stateshaper* *'Connector'* class to define specific rules for the tokens included in 'vocab' list. This can be based on developer needs and can be based on attributes, sequence or frequency the tokens are called if needed.



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



## Use Cases


### Personalization Without Storing User Data

Personal Ads or News
Fitness Routine
Smart Home Scheduling
NPC Behavior

Assign each user a seed and derive their long-term content pattern from it, without storing
behavioral data or personally identifiable information.


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
├── src/
│   └── main/
│       ├── __init__.py
│       ├── connector.py
│       ├── core.py
│       ├── demo.py
│       ├── run.py
│       └── connector/
│           ├── __init__.py
│           ├── Connector.py
│           ├── Modify.py
│           ├── Vocab.py
│       └── demos/
│           ├── __init__.py
│           ├── ads/
│               ├── __init__.py
│               ├── ad_list.py
│               ├── Ads.py
│       └── tools/
│           ├── __init__.py
│           ├── tiny_state/
│               ├── __init__.py
│               ├── TinyState.py
│           ├── morph_rules.py
│           ├── seeds.py
│           ├── semantic_mapper.py
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── setup.py
├── requirements.txt
└── .gitignore
└── demo.bat
└── run.bat
```



## Contributing

Contributions, ideas, and experiments are welcome!

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

---

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.

If you use this in research, products, or experiments, a mention or citation of the
"Morphic Semantic Engine" is appreciated.
