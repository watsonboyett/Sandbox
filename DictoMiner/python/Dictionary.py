

""" Container class for a collection of words """


class Dictionary:
    
    def __init__(self):
        """ Empty constructor - initialize the object """
        self.words = {}
        self.count = 0
    
    # --------------------------------------------------------------- #
    
    def add_word(self, word):
        """ add a word to the dictionary's list of words """
        self.words[word.string] = word
        self.count = self.count + 1
        
    def get_word(self, word_str):
        """ return a word that matches the given input string """
        return self.words[word_str]
    
    def get_words_iter(self):
        """ return an iterator over the entire list of words """
        return self.words.itervalues()
    
    def get_wordlist(self):
        """ return the list of word strings """
        return [w for w in self.words]

    
    
    