# Morphic Semantic Engine (MSE)

**Compress data and generate content using small seeds.**

*Clean up database tables by generating data in real-time within your app.*


The origin of this idea started with the 'Infinite Map Concept' I created in early 2025. The core logic starts with the idea of using a static length array of numbers which has values that change based on a mathematic function. The function uses a modulus operator to keep the array within a fixed range of values. Because of this, continuing to run the engine will produce an unbound chain of deterministic output. 

Using a custom plugin file, events can be mapped to the array by tokenizing its values. The engine allows for the events be called for as long as needed. The events can include many types of data including strings, links, images and functions. Due to the nature of the algorithm, the mapped events can be condensed and extracted as the MSE runs.

This idea was improved upon with some help from ChatGPT, and has become the Morphic Semantic Engine.

Recommended Uses Include:

- Synthetic data generation
- Deterministic simulations
- Procedural text & lore
- Privacy-safe personalization
- Embedded / offline generative behavior

This repository contains a reference implementation in Python, example scripts, and documentation.

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
git clone https://github.com/jgddesigns/mse.git
cd mse
pip install -r requirements.txt
```

---


## Basic Example

The MSE uses an evolving array of numbers that can be tokenized to call events or variables. 


```python
from main.core import MorphicSemanticEngine
from main.plugin import PluginData

# Small numeric seed (arbitrary integers unless otherwise needed). These values are the starting array to base the math on. Their state is what the vocab data is called from from. The array length stays consistant as the numbers change. 
seed = [12, 7, 4, 19, 3, 11, 5, 8, 2]

# Minimal vocabulary (these tokens can mean anything in your app). For instance, this set of numbers is chosen based on a rating system in the plugin file. When tokenized, they can call desired output from the plugin. They can be modified as the engine runs if the output needs to be changed. This allows for personalization and can be based off of variables such as user behavior. 
vocab = [1, 2, 3, 6, 7, 9]

# Class instantiation. The parameters are the only values that need to be stored other than your app's custom plugin file. In the most minimal cases, only the vocabulary is needed to be stored.
engine = MSE(
    initial_state=seed,
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


# Plugin Data

A custom plugin can be tailored to an app's specific purpose. This is what will set the rules for what data or events are to be called as the MSE runs. All that is needed from the plugin is a final list to be used in the 'vocab' parameter. This can be compressed and all that is the only thing needed tp be stored in a database. 

The current standard is to keep several columns and rows of specific data. With the MSE, this data can be generated in real time using only the seed and the package's included calculations. 


```python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core import MSE
import json


class PluginData:
   engine = MSE()

   # Here is an example of a map of events that can be called from the specified MSE vocab. They can be random, personalized, or called in a specific sequence.
   event_map = {
      1: show_ad("adhost.ad_list.ad_link_001")
      2: show_ad("adhost.ad_list.ad_link_002")
      3: show_ad("adhost.ad_list.ad_link_003")
      4: show_ad("adhost.ad_list.ad_link_004")
      5: show_ad("adhost.ad_list.ad_link_005")
      6: show_ad("adhost.ad_list.ad_link_006")
      7: show_ad("adhost.ad_list.ad_link_007")
      8: show_ad("adhost.ad_list.ad_link_008")
      9: show_ad("adhost.ad_list.ad_link_009")
   }

   #The event ratings determine what ads will be put in the MSE vocab. This can be modified over time based on input such as user behavior. The ratings can stand for anything such as:
   #
   #  drinks = {"beer" 67, "wine": 85, "tea": 86...etc}
   #
   # They can then be used to call ads for those preferences. 
   ratings = {
      1: 45,
      2: 78,
      3: 3,
      4: 43,
      5: 98,
      6: 67,
      7: 89,
      8: 54,
      9: 92,
   }

   def adjust_ratings(rating, input):
      self.ratings[rating] += input

   #Stopped drinking beer for a week and drank more tea.
   adjust_ratings("beer", -5)
   adjust_ratings("tea", 3)

```


# Tiny MSE Format

Aside from the plugin file (which can be a template that does not include specific numbers), relevant data such as the event map and ratings can be condensed into 'Tiny MSE' and/or 'Raw MSE' format. Example:

Tiny MSE: ABC-12345

Raw MSE: QV589JX4

These values can be encoded and decoded in the TinyMSE class within the 'tools' directory. The main data map is represented as a long string of numbers. These numbers stand for positions in the map and are encoded into Tiny MSE format. A subset of numbers from the vocab used in the engine is also kept and encoded into Raw MSE format.


```python 
class TinyMSE:

   def encode_tiny(data):
      # Encode logic
      # This is the value that will be kept in the database. It is where most of the compression happens. 
      # This value 
      return "ABC-12345"

   def decode(data):
      # Decode logic.
      # These values stand for key/value pairs from the event or ratings maps and are kept in groups of four in data sets length 100 or less. If more length is needed the group size can be increased.
      #
      # Example: 0214 stands for key #3, value #15 

      return 0011011202130314...

```

 
For a given user, all that will be needed to be stored for the above example is:

["user-1234", ["abc-12345", QV589JX4]]

From that, all other content can be generated during run time, and be personalized to each user. 

The ratings can be modified as needed, then re-encoded as a different seed. 

For some uses, a longer seed may be required. Sometimes this can be because a custom initial state, mod or constants are  required. Also if a very large amount of data causes the Tiny MSE seed to need additional characters. 



---

## How It Works (High-Level)

1. **Seed** – You start with a small fixed-length array of integers (e.g. 9 numbers).
2. **Morph Rule** – On each step, the array is updated using a deterministic formula that
   combines the current value, the constant values, modulus, and the iteration index. The modulus value keeps the array values witin a certain range. This allows for unbound deterinism because whenever a specific number is processed, the resulting number will always be the same.
3. **Code Extraction** – The engine summarizes the state into a small integer "code"
   using weighted sums and offsets.
4. **Semantic Mapping** – The code is mapped into a vocabulary index, producing a token.
5. **Feedback** – The previously chosen token influences the next mapping, so the "meaning" evolves with the state.

The result is a compact engine that turns tiny seeds into large, evolving sequences that feel
structured and consistent over time.

---

## Use Cases


### Personalization Without Storing User Data

Assign each user a seed and derive their long-term content pattern from it, without storing
behavioral data or personally identifiable information.


### Synthetic Data 

Generate large, reproducible datasets (e.g. sensor readings, event streams, synthetic markets)
from a single small seed. This avoids privacy issues and reduces cost compared to collecting
real-world data.






---

## Project Structure

```text
mse/
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
│           ├── tiny_mse/
│               ├── __init__.py
│               ├── TinyMSE.py
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
