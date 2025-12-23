# Contributing to Stateshaper


Stateshaper can do a lot on its own, but does even better with Shaper Plugins! 

Plugins are intended to define what events are called using the engine. This can be specific to each app, but can also apply to other app's with similar logic.

Plugins for random events, ratings based personaliation, pure compression and structured output are planned to be released as standard universal add-ons to the library.

If a user can some up with their own specialized Shaper Plugin, sharing it would be appreciated! The open source aspect of Stateshaper is encouraged. 



Here is an example of how a plugin is used:


Stateshaper can create continued meaningful output using very little memory. 

The ouput created needs to be defined somehow. 

This can be based on preference (ex. using a rating system), at random, as a specific sequence, or a combination of these. 




-------


**Personalization Example**


Define entire dataset for terms used in app. 

For this example, a meal planner. This type of plugin can also be used for applications like fitness routine, gaming npc behavior and personalized content. Here is an example with a small dataset. 

```python
terms = {
    0: {"steak and eggs": ingredients1, "rating": 76},
    1: {"enchiladas": ingredients2, "rating": 61},
    2: {"risoto": ingredients3, "rating": 88},
    3: {"chicken and dumplings": ingredients4, "rating": 34},
    4: {"corn salad": ingredients5, "rating": 55},
    5: {"macaroni and cheese": ingredients6, "rating": 15},
    6: {"shrimp egg rolls": ingredients7, "rating": 32}
}
```

A normal list might hold hundreds, thousands or even more values. This is the data that needs to be hardcoded into an app. As it relates to a specific user, it can be significantly condensed in database tables when using Stateshaper. The ratings allow for only certain values to be called from the master list.

In this example, the ratings used can be modified. Here is a function that listens for events used to change the ratings. This is pseudocode, assuming there is a meal tracker and a feature where users can like meals that are shown on screen.  

For personalization data, the objects the logic is based on can be compressed into *Tiny State* format using the *TinyState* class. 

See the *TINY_STATE.md* instructions in *src/main/tools/tiny_state*


```python

# @param event 
#
# ex. like a meal featuring shrimp
# ex. {"shrimp" like_score}
#
# ex. don't eat beef for 2 weeks
# ex. {"beef", inactive_score * days}
# 
#
# @param trend 
# an array featuring normalized values of food intake
#
def listener(event, trend):
    ## User has indicated they have an increased preference in seafood, and hasn't eaten meals with beef in them for three weeks. 

    # likes a seafood meal in content feed
    trend["shrimp egg rolls"] = modify(trend[event], .05)
    
    # meal tracker shows user hasn't eaten beef in two weeks
    trend["steak and eggs"] = modify(trend[event], -.15)


def modify(rating, change):

    rating += change


```


-------


**Synthetic Data Example**

This example is for Fintech Quality Assurance Testing. Synthetic data is continually generated to stress the application and expose weak points.

A collection of terms is created for each test case. In this case, a system that stress tests an app's ability to detect fraud. 

Similar uses include economy simulations, UUID creation and other QA compliance uses.

One of the main benefits here instead of using a hardcoded loop is that every test case (as many as needed) can be recreated from the ~225 byte State Seed.


```python

user = ["profile", "contact", "session", "bank", "indentity"]

addresses = ["none", "partial", "full"]
conditions = [True, False]
phones = ["mobile", "landline", "voip", "toll_free", "unknown"]

# create a faux user to enter into the system
user = {
    "profile": {
        "name_match": random_choice(conditions, step),
        "dob_match": random_choice(conditions, step),
        "address_match": random_choice(addresses, step)
    },
    "contact": {
        "phone_new": random_choice(conditions, step),
        "email_new": random_choice(conditions, step),
        "phone_type": random_choice(phones, step)
    },
    "session": {
        "failed_logins": random_attempts(conditions, step),
        "new_device": random_choice(conditions, step),
        "new_ip_country": random_choice(conditions, step),
        "password_reset": random_choice(conditions, step)
    },
    "bank": {
        "micro_deposit_failures": random_choice(conditions, step),
        "account_changes": random_attempts(conditions, step)
    },
    "identity": {
        "ssn_format_valid": random_choice(conditions, step),
        "credit_header_match": random_choice(conditions, step)
    }
}


def random_choice(value, step):
    return round(step % 10/len(value) * .01)


def random_attempts():
    return randint(0, step*.001 * 20)

vocab = [adresses, conditions, phones] 

## Connector passes to Stateshaper. Program generates a random test case. All test cases are memorized ansd can be extracted from the seed at any time.
Connector(vocab)


```


-------


**Procedural Generation**



Functions are called during each iteration of the engine. The parameters accept the current array value and create content based on their values. 

The same benefit here as the last case, determinism. With more logic to define the map assets, an entire world can be memorized and built from a Stateshaper seed.


```python


data = [event1(step), event2(step), event3(step), event4(step), event5(step), event6(step)]


def create_content(step):

    shape = Draw(
                pos = get_pos(step),
                color = get_color(step),
                shape = get_shape(step),
                size = get_size(step)
            )

def get_pos(step):
    return (step/window_width * 100, step/window_height * 100)


def get_color(step):
    colors = []
    while len(colors) < 4:
        colors.append(int(round(step%100).01))

    return tuple(colors)


def get_shape(step):
    shape = []
    path = [0, 0]
    while len(shape) < (step % 10):
        side = round(step*.01)
        vertical = round(step*.01) 
        directions = (0 if round(step*.01) < .5 else 1, 0 if round(step*.01) < .5 else 1)   
        x = side * directions[0]
        y = vertical * directions [1]
        path = [path[0] += x, path[1] += y]
        shape.append(path)

    return shape


def get_size(step):
    width = step % 1000 / randint(1, step % 3 if step % 3 or 2)
    height = step % 1000 / randint(1, step % 3 if step % 3 or 2)

Connector(data)


```


-------


**Structured Sequence**


Map a list of events or variables to pre-determined output.



```python

events = {
    0: event1,
    1: event2,
    2: event3,
    3: event4
}

# The outputed is always the same based on the seed.

output = [145, 647, 45, 784, 567, 432...]


# events are called every time their assigned number appears. one even can have several numbers mapped to it. 

map = {
    0: [145, 784],
    1: [647],
    2: [45, 567],
    3: [432]
}

vocab = [0, 1, 2, 3]


Connector(vocab)

```



Right now this type of use is limited, but expansion for structured output is currently in ***experimental*** stages. Theorhetically, if a grid of all possible Stateshaper arrays can be built, nearly any type of data coded can be compressed and re-built with the Stateshaper engine. 

This grid would be massive, and require the assistance of AI to be built. 

Think of the array values as steps for a recipe. Cooking a recipe correctly requires you to follow the steps in order. Now imagine all possible recipes, some have different steps and some matching but in a different order. To cook them all, we'd need to be able to generate every possible combination of steps. 

Another (and one of the most difficult) example is written language. There are many possible combinations of words to form sentences, chapters and entire books. Compressing this into a seed has limits based on Shannon's theory, but with the right set of rules using Stateshaper might be able to find a possible workaround. Until recently, this would have been near impossible, but with the release of moder AI tools, creating the backend logic needed to do this has become easier. 


Current Experimental Ideas:

- Create a known list of possible arrays the Stateshaper can produce, and a tool that allows for the required output to be compressed into a State Seed.
- Add a length limit option to cut down the reasonable amount of possible arrays needed.
- Write a morph function creator that is used to create arrays that arent possible with the default morph function.
- If a particular set of data can't be built from the known arrays, use AI to brute force compare each missing value and write rules to a matching array.
- A Stateshaper grid tool is planned to be released soon. This will help find the rules needed to build certain types of data based on known existing arrays. 