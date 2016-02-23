

""" Parser for the Diceware dataset """

import re
import sys

from Dictionary import Dictionary
from Word import Word


class Diceware:
    fname = r'../data/diceware_wordlist.txt';
    
    @staticmethod
    def get_dictionary( ):
        """ Build a Dictionary based on the Diceware data. """
        
        dicto = Dictionary()
        
        print 'Parsing Diceware data...'
        i = 0;
        nLines = 7780
        
        # open file for reading
        with open(Diceware.fname, 'r') as fid:    
            for line in fid:
                tokens = Diceware.parse_line(line)
                if tokens is None:
                    continue
                
                # save data to list
                word = Word(tokens['word'], -1, -1, i);
                dicto.add_word(word)
                
                # increment counter and show progress
                i = i + 1;
                progress = float(i) / float(nLines)
                if (progress % 0.05) < 1e-4:
                    sys.stdout.write("\r%2.2f%%" %(progress*100))
                    sys.stdout.flush()
                    
        print '\nDone.'
        
        return dicto

    @staticmethod
    def parse_line(line):
        """ Parse a single line of the Diceware dataset. """
        
        tokens = line.split()
        # skip empty and malformed lines
        if len(tokens) == 2:
            data = {}
            data['word'] = tokens[1].upper()
            data['key'] = tokens[0]
        else:
            data = None
            
        return data
    
if __name__ == "__main__":    
    dicto = Diceware.get_dictionary()


