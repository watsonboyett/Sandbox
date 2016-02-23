

""" Container class for a word (string) and its attributes """


class Word:

    def __init__(self, string, count=0, prob=0, loc=0):
        """ initialize (and calculate metrics for) the given string """
        
        self.set_string(string)
        self.count = count
        self.prob = prob
        self.loc = loc
    
    # --------------------------------------------------------------- #
    
    def set_string(self, string):
        """ update atributes for the given string """
        
        self.string = string
        self.length = len(string)
        self.chars = set(string)
        self.chars_n = len(self.chars)
    