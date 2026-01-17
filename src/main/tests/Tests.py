
import random



class Tests:


    def __init__(self, debug=True, **kwargs):
        

        

    
    # creates chain of deterministic output based on seed, then steps backward to see if the same output can be recreated. if so, this indicates deterministic states that can be traversed both forward and in reverse. 
    def reversibility(self, engine, x):
        print("\n\n\n\nREVERSIBILITY TEST\n\n")
        print("\n" + engine["compare"].upper() + "\n")
        print("\n\nforward step\n")
       
        forward = engine["forward"](x)
        print(forward)
        print("\n\n\nreverse step\n")
        reverse = engine["reverse"](x)
        print(reverse)
        
        result = True if list(reversed(reverse)) == forward else False
        
        print(engine["compare"].upper() + " Test Result: " + str(result) + ", list is reversible.")
        
        return result
    

    # creates output based on seed parameters, then attempts to recreate that output using the same seed. matching outputs confirms that the seed creates a deterministic sequence. 
    def determinism(self, engine, x, existing):
        print("\n\n\n\nDETERMINISTIC TEST\n\n")
        print("\n" + engine["compare"].upper() + "\n")
        print("\n\nfirst output\n")
        print(existing)

        print("\n\nsecond output\n")
        current = engine["run"](x)
        print(current)

        result = True if existing == current else False
        print(result)
        
        print(engine["compare"].upper() + " Test Result: " + str(result) + ", lists are matching.")
        
        return [result, current]
    

    # tests are based on data that is needed to store memory for a personalized video game npc. this particular test is meant to represent 10 decisions the npc previously made based on their attributes, and the ratings used to influence future decisions. the original data includes a list of sample actions and preference ratings. the items are compressed into stateshaper format with values that stand for the position in the dictionary the decisions occur in, along with their ratings. the standard data takes the positions of the decision in the dictionary, and ratings for each type of decision. 
    #
    # the stateshaper engine allows for these events to be ran continuously, with privacy through obfuscaation, minimal storage space used, and the ability to alter the stream along the way 
    #
    # stateshaper
    # 
    # {"s":[66,67,54,3,34],"v":["AAA01005","578ACDEXF"]}
    # 
    # "s": the initial state used to start the engine
    # "v": the compressed vocab used in the engine. v[0] is the compressed seed for the whole data pool, including ratings. v[1] is only the memory of decisions that were made.
    #
    # standard ("r" can increase depending on size of data object)
    #
    # {"s":[0, 4, 5, 6, 2, 2, 2, 5, 6, 8], "r": [9, 67, 35, 76, 35, 67, 75, 98, 57, 95]}
    #
    # "s": places in the data that memorize what was called
    # "r" : the ratings for the data that is called
    #
    def compression(self, length, compare):
        compare = compare.upper()
        data = "data = {'is starting to attack you!': 67, 'assumes a guarded position!': 83, 'is asking if you have anything to trade...': 41, 'runs and hides when they see you!': 23, 'asks if you want to join...': 89, 'is offering to help with your cause...': 53, 'wants to know where the nearest town is...': 26, 'is asking if you can repair their wagon...': 98, 'looks confused upon seeing you...': 56, 'draws their weapon cautiously...': 72, 'waves at you from a distance...': 34, 'demands to know your business here!': 91, 'greets you with a friendly smile...': 18, 'backs away slowly, watching your moves...': 64, 'offers to sell you supplies...': 47, 'warns you about dangers ahead...': 85, 'asks if you have seen anyone suspicious...': 29, 'sizes you up without saying a word...': 76, 'calls for help from nearby allies!': 94, 'asks if you are lost...': 12, 'offers you a place to rest...': 58, 'threatens you if you come closer!': 88, 'is clearly relieved to see you...': 21, 'keeps their distance but stays alert...': 69, 'asks if you need medical assistance...': 37}..."

        stateshaper = '{"s":[66,67,54,3,34],"v":["AAA01005","578ACDEXF"]}'
        other = '{"s":[0, 4, 5, 6, 2, 2, 2, 5, 6, 8], "r":' + self.get_ratings(length) + '}'

        
        print("\n\nTINY_STATE test comparison for " + str(length) + " items")
        
        print("Original Data Sample Format (length varies):\n")
        print(data)
        
        print("STATESHAPER Stored Data Size - " + str(len(stateshaper)) + " bytes\n")
        print(stateshaper)
        
        print("STANDARD Stored Data Size - " + str(len(other)) + " bytes\n")
        print(other)
        

        print("STATESHAPER is smaller than " + compare + " by " + self.get_percent([len(stateshaper), len(other)]) + "%" if len(stateshaper) < len(other) else compare + " is smaller than STATESHAPER by " + self.get_percent([len(other), len(stateshaper)]) + "%" if len(other) < len(stateshaper) else "Both algorithms have an equal storage size.")

        


    def get_ratings(self, length):
        ratings = []
        while len(ratings) < length:
            ratings.append(random.randint(1, 100))
        return str(ratings)


    def get_percent(self, compare):
        return str(int((compare[1]-compare[0])/compare[1] * 100))