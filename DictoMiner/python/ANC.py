

""" Parser for American National Corpus dataset """

import re
import sys

from Dictionary import Dictionary
from Word import Word


class ANC:
    fname = r'../data/ANC-token-count.txt';
    
    @staticmethod
    def get_dictionary( ):
        """ Build a Dictionary based on the American National Coprus data. """
        
        dicto = Dictionary()
        
        print 'Parsing ANC data...'
        i = 0;
        nLines = 240000
        
        # open file for reading
        with open(ANC.fname, 'r') as fid:    
            for line in fid:
                tokens = ANC.parse_line(line)
                if tokens is None:
                    continue
                
                # save data to list
                word = Word(tokens['word'], tokens['count'], tokens['prob'], i);
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
        """ Parse a single line of the ANC dataset. """
        
        tokens = line.split()
        # skip empty and malformed lines
        if len(tokens) == 3:
            data = {}
            data['word'] = tokens[0].upper()
            data['count'] = int(tokens[1])
            data['prob'] = float(tokens[2])
        else:
            data = None
            
        return data
    
if __name__ == "__main__":    
    dicto = ANC.get_dictionary()

