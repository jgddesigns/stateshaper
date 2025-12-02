# Mathematical Details

The default morph rule is:

```text
new[i] = (a * state[i] + b * state[i-1] + c * t + d) mod M
```

Where:
- `state[i]` is the current cell value.
- `state[i-1]` is the previous cell (with wraparound).
- `t` is the iteration step (0, 1, 2, ...).
- `a, b, c, d` are small integer constants.
- `M` is a modulus.

A code is derived by taking a weighted sum of the state, plus the current
iteration counter, and applying a small modulus (e.g., 27). This code is
combined with an offset based on the state sum and the previous token index
to select a token index in the vocabulary.

The morph rule can be changed according to the desired output. Doing so allows for the produced chain of values to be altered. An example of why this migh be necessary is if a user decides they need a value to occur in repetition or on a certain schedule.