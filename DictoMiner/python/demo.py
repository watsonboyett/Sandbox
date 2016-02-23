

""" A simple example to demonstrate the high-level usage of the DictoMiner project """


from ANC import ANC
from DictoMiner import DictoMiner
from DictoPlotter import DictoPlotter

# build dictionary from ANC text file
dicto = ANC.get_dictionary()

# gather stats of dictionary
dm = DictoMiner(dicto)

# show views of different stats
DictoPlotter.demo(dm)


