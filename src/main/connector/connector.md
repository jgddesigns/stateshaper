**HOW TO USE PLUGIN CONNECTOR**


---


1. Make sure you have your events and corresponding prefence ratings mapped in the proper format. Example:

        ```python

        {
            "input": [
                {
                    "data": "grilled chicken salad",
                    "rating": 14
                },
                {
                    "data": "spaghetti bolognese",
                    "rating": 14
                },
                {
                    "data": "vegetable stir fry",
                    "rating": 14
                },
                {
                    "data": "cheeseburger",
                    "rating": 45
                },
                {
                    "data": "pepperoni pizza",
                    "rating": 88
                },
                {
                    "data": "fish tacos",
                    "rating": 35
                },
                {
                    "data": "beef burrito",
                    "rating": 75
                },
                {
                    "data": "chicken alfredo",
                    "rating": 65
                },
                {
                    "data": "lentil soup",
                    "rating": 25
                },
                {
                    "data": "bbq ribs",
                    "rating": 92
                },
                {
                    "data": "avocado toast",
                    "rating": 3
                },
                {
                    "data": "shrimp fried rice",
                    "rating": 55
                },
                {
                    "data": "pancake breakfast",
                    "rating": 77
                }
            ],

            "rules": "rating",
            "length": 10,
        }

        ```

        input:
            data: Can be any data type. For instance, a string, number or function. This is what will be called as the Stateshaper Engine is running. 
            rating: This is the preference rating for each item in the input list. A higher rating will be added with priority. 

        rules:
            In this case the rule is always "rating" due to the data being used for personalization. Other examples for compound, random, and token will be listed at the end of the file.

        length:
            The length of the vocab list to be passed into the engine. This is what will be called as the engine runs. 

2. Call 'Connector' class, passing the above data object as a parameter. 

3. To get the seed to pass into the engine, call the Connector function, start_connect. 


---


**Modification**


These functions are part of the Connector class. When used, the ratings associated with events can be adjusted. This has a direct effect on the personalization of the output. In other words, the events with the highest ratings will occur more frequently in the stream created by the engine. If a length is set in the main data object, only the values with the highest ratings will be included in the engine vocab. 


```python
set_value(key, rating)
```

*Sets the value of a specific item in the data input object.*

```python
adjust_value(key, adjust)
```
    
*Adds or subtracts the rating for a specific item.*


```python
alter_stream() 
```

**REQUIRED**

*After changing a rating value or values, returns the seed used in the Stateshaper engine. If the function is not called, the stream will not be modified.*