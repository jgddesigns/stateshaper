# *Stateshaper*

*Create many types of content from a small seed*

<br>
<br>
<pre>
pip install stateshaper
</pre>

<br>
<br>

<pre>
git clone https://github.com/jgddesigns/stateshaper.git
</pre>

<br>
<br>

*Stateshaper* is an infinite data generator. 

It is most effective for applications involving synthetic data, personalization and world building. 

The parameters entered into *Stateshaper* effect what output will be produced. 

Numeric values are returned that can be tokenized and used to derive data such as variables, rule-sets, function triggers, build sequences and more. 

It is lossless, indexible and reversible. Storage size is less than 50 bytes.

<br>
<br>

Basic Example:

```python
from stateshaper import Stateshaper

# Parameters only need to be included if a variation in output is needed.
stateshaper = Stateshaper() 

# With parameters (not required)
#
# initial_state - The number where the math starts. Can be any positive whole number.
# constants - Used for variety in the output. Can be any positive whole numbers.
# mod - The maximum token value. Set higher to more effectively approach infinite output.
stateshaper = Stateshaper(initial_state=1, constants={"a": 3,"b": 5,"c": 7,"d": 11}, mod=9973)

stateshaper.start_engine()

# Get 50 tokens 
token_array = stateshaper.run_engine(50)

# Get one token
token = stateshaper.one_token()

# Reverse 50 places
reverse = stateshaper.reverse(50)

# Jump to token 1,000,000
forward = stateshaper.jump(1000000)
```


<br>
<br>

Output Example:

```python
[3478, 583, 72, 8931, 4566]
```

<br>
<br>

Use Example:

```python
value = token % max_value

# Add more rules to create values as needed. 
```

<br>
<br>

---

<br> 

## Project Structure

```text
stateshaper/
├── src/
│   └── main/           
│       ├── core.py
│       ├── stateshaper.py
├── LICENSE
├── pyproject.toml
├── QUICK_START.md
├── README.md
├── setup.py
```

<br> 

---

<br> 

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.

If you use this in research, products, or experiments, a mention or citation of the
"*Stateshaper*", "Jason Dunn", and/or "jgddesigns" is appreciated.
