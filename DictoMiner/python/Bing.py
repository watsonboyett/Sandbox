

""" Parser for Bing's web-crawler dataset """

import re
import sys

from Dictionary import Dictionary
from Word import Word


class Bing:
    fname = r'../data/Bing-Apr10.txt';
    
    @staticmethod
    def get_dictionary():
        """ Build a Dictionary based on the Bing's web data. """
        
        dicto = Dictionary()
        
        print 'Parsing BingBody data.'
        i = 1;
        nLines = 100000
        
        # open file for reading
        with open(Bing.fname, 'r') as fid:    
            for line in fid:
                tokens = Bing.parse_line(line)
                if tokens is None:
                    continue
                
                # save data to list
                word = Word(tokens['word'], -1,-1, i);
                dicto.add_word(word)
                
                # increment counter and show progress
                i = i + 1;
                progress = float(i) / float(nLines)
                if (progress % 0.05) < 1e-4:
                    sys.stdout.write("\r%2.2f%%" %(progress*100))
                    sys.stdout.flush()
                    
        print 'Done.'
        
        return dicto
    
    @staticmethod
    def parse_line(line):
        """ Parse a single line of the Bing dataset. """
        
        tokens = line.split()
        # skip empty and malformed lines
        if len(tokens) == 1:
            # save data to list
            data = {};
            data['word'] = tokens[0].lower();
        else:
            data = None 
            
        return data                
        

if __name__ == "__main__":
    dicto = Bing.get_dictionary()

    

