# allow for encoder/decoder to expand based on signal value -. - indicates another child in that item. the string terminates with another -. for nested children, a - followed by -. 
#593058- --> child in item --> 346729573-- --> another child --> 18365342- --> end of item


##for json data templates that are repeatedly used...
class CompressJson:


    def __init__(self, **kwargs):
        



    def compress(self, data):
        levels = self.get_levels(data)


    # creates index string of matching data based on an item's position in a json dict. determines if the item is nested and at what level.
    # data - the dict of data
    # current - a list of items to check against the data
    # levels - an ongoing list of position index values
    # level (recursion) - if a nested value is found, this is used to define the value
    # parent (recursion) - if a nested value is found, this is used to define the parent of the value 
    def get_levels(self, data, current, i=0, levels=[], level=None, parent=None):
        if not level and i < len(data):
            while i < len(data):
                for child in data[i]:
                    if self.list_check(child):
                        i += 1
                        return self.get_levels(data, current, i, levels, child, data[i])
                    levels.append([f"{i:02d}", f"{0:02d}"]) if self.list_compare(data[i], current) else None
                i+=1
        elif level and i < len(data):
            levels.append("-")
            for item in level:
                for child in item:
                    if self.list_check(child):
                        levels.append("--")
                        return self.get_levels(data, current, i, levels, child, level.index(item))
                    levels.append([f"{parent:02d}", f"{level.index(item):02d}"]) if self.list_compare(item, current) else None 
            levels.append("-")      
            return self.get_levels(data, current, i, levels, item)
        else:
            return "".join(levels)


    def list_compare(self, item, current):
        try: 
            if len([i for i in list(item.keys()) if i in current]) > 0: 
                return True
        except:  
            if len([i for i in item if i in current]) > 0: 
                return True        
        return False
    

    def list_check(self, item):
        if len([i for i in item if isinstance(i, dict) or isinstance(i, list)]) > 0:
            return True
        return False
    

    # get pos and deepness of a particular item
    def get_level(self):
        pass
        












