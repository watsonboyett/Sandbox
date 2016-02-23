

""" Gathers statistical information about different lexicons (e.g ANC, BingBody, etc.) """

import pdb
import re
import numpy as np

from Dictionary import Dictionary


class DictoMiner:
    
    def __init__(self, dicto):
        # TODO: make deep copy of dictionary?
        # (so we don't destroy original in processing steps)
        self.dicto = dicto
        
        self.preproc()
        self.proc()
        
    # --------------------------------------------------------------- #
 
    def preproc(self):
        """ normalize the data (clean/remove problematic characters) for processing """

        print 'Pre-processing dictionary...'
        
        # remove words that contain non-alphanumeric characters
        dicto_new = Dictionary()
        alpha = re.compile('[\W]')
        num = re.compile('[0-9]')
        for word in self.dicto.get_words_iter():
            word_str = word.string
            
            # remove numbers from words
            word_str = num.sub('', word_str)
            if len(word_str) <= 0:
                continue
            
            if not alpha.search(word_str):
                word.set_string(word_str)
                dicto_new.add_word(word)
                
        print 'Done.'
        
        self.dicto = dicto_new
        
    def proc(self):
        """ calculate metrics about the given dataset """
        
        print 'Gathering metrics on dictionary...'
        
        # gather all word strings
        self.words = [w.string for w in self.dicto.get_words_iter()] 
        self.words_n = self.dicto.count
        
        # gather word lengths (and their frequency distribution)
        self.wordlen_list = [w.length for w in self.dicto.get_words_iter()] 
        dist = DictoMiner.get_length_dist(self.wordlen_list)
        self.wordlen_set = dist['edges']
        self.wordlen_set_n = len(self.wordlen_set)
        self.wordlen_set_dist = dist['vals']
        self.wordlen_set_norm = dist['norm']

        
        # gather list of all characters
        word_strs = [word.string for word in self.dicto.get_words_iter()]
        self.charlist = ''.join(word_strs)
        self.charlist = self.charlist + ' '
        self.charlist_n = len(self.charlist)
        
        # gather set of unique characters (and their frequency distribution)
        dist = DictoMiner.get_letter_dist(self.charlist)
        self.charset = dist['edges']
        self.charset_n = len(self.charset)
        self.charset_dist = dist['vals']
        self.charset_norm = dist['norm']
        # create LUT for fast oridinal indexing
        self.charset_lut = {ord(self.charset[i]): i for i in range(self.charset_n)}
 
        print 'Done.'

    # --------------------------------------------------------------- #

    # TODO: remove this function in favor of generic freq. dist. below
    @staticmethod
    def get_letter_dist(chars):
        """ calculate letter frequency distribution """
        
        # get single letter distribution
        char_conv = np.array([ord(c) for c in chars])
        char_set = np.unique(char_conv)
        char_set = np.append(char_set, char_set[-1]+1)
        char_edges = np.sort(char_set)
        char_dist = np.histogram(char_conv, char_edges)[0]
        
        # attempt to normalize
        norm_meth = 1
        if norm_meth == 1:
            norm_str = 'Percentage'
            norm_val = float(len(chars))
        else:
            norm_str = 'None'
            norm_val = 1

        char_dist = [cd/norm_val for cd in char_dist]

        # sort by frequency (descending)
        dist = {}
        ix = np.argsort(char_dist)
        ix = ix[::-1]
        dist['vals'] = [char_dist[i] for i in ix]
        dist['edges'] = [chr(char_edges[i]) for i in ix]
        dist['norm'] = norm_str
        return dist
    
    # TODO: make this function more generic
    # (so it can be used for letter freq. dist.)
    @staticmethod
    def get_length_dist(word_lens):
        """ calculate world length distributions """
        
        # get word length distribution
        len_min = min(word_lens)
        len_max = max(word_lens)
        edges = np.arange(len_min, len_max)
        vals = np.histogram(word_lens, edges)[0]
        
        # attempt to normalize
        method = 1
        if method == 1:
            norm_str = 'Percentage'
            norm_val = float(len(word_lens))
        else:
            norm_str = 'None'
            norm_val = 1
        
        vals = [v/norm_val for v in vals]

        # save results
        dist = {}
        dist['vals'] = vals
        dist['edges'] = edges
        dist['norm'] = norm_str
        return dist


if __name__ == "__main__":
    from ANC import ANC

    try:
        dicto = ANC.get_dictionary()
        dm = DictoMiner(dicto)
    except Exception as e:
        print e

        import sys
        tb = sys.exc_info()[2]
        pdb.post_mortem(tb)
    
    
    
