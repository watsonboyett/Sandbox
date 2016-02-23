
class Piece:

    tiles = []
    pos = [0,0]
    id = 0
    cover = []

    order = 0       # number of filled tiles in piece
    key = 0         # unique id of piece (rot. invariant)
    conf = 0        # rotation of piece
    color = 0       # color of piece


    def __init__(self,tiles):
        self.tiles = tiles


    def check_overlap(self,other):
        # ensure that both pieces cover a part of the board
        if len(self.cover) < 1 or len(other.cover) < 1:
            return True
    
        # ensure that they don't overlap
        isect = filter(set(self.cover).__contains__,other.cover)
        if any(isect):
            return True
    
        # pieces do not overlap
        return False



    @staticmethod
    def rot_90(tiles):
        #tiles = zip(*tiles)[::-1]

        nRows = len(tiles)
        nCols = len(tiles[0])
        tmp = [[0 for r in range(nRows)] for c in range(nCols)]
        for r in range(nCols):
            for c in range(nRows):
                tmp[r][c] = tiles[nRows-c-1][r]
        return tmp

    @staticmethod
    def rot_180(tiles):
        #tiles = zip(*tiles)[::-1]

        nRows = len(tiles)
        nCols = len(tiles[0])
        tmp = [[0 for c in range(nCols)] for r in range(nRows)]
        for r in range(nRows):
            for c in range(nCols):
                tmp[r][c] = tiles[nRows-r-1][nCols-c-1]
        return tmp

    @staticmethod
    def rot_270(tiles):
        #self.tiles = zip(*self.tiles[::-1])

        nRows = len(tiles)
        nCols = len(tiles[0])
        tmp = [[0 for r in range(nRows)] for c in range(nCols)]
        for r in range(nCols):
            for c in range(nRows):
                tmp[r][c] = tiles[c][nCols-r-1]
        return tmp

    @staticmethod
    def mirror_horz(tiles):
        nRows = len(tiles)
        nCols = len(tiles[0])
        tmp = [[0 for r in range(nCols)] for c in range(nRows)]
        for r in range(nRows):
            for c in range(nCols):
                tmp[r][c] = tiles[r][nCols-c-1]
        return tmp

    @staticmethod
    def mirror_vert(tiles):
        nRows = len(tiles)
        nCols = len(tiles[0])
        tmp = [[0 for r in range(nCols)] for c in range(nRows)]
        for r in range(nRows):
            for c in range(nCols):
                tmp[r][c] = tiles[nRows-r-1][c]
        return tmp

    @staticmethod
    def transpose(tiles):
        nCols = len(tiles)
        nRows = len(tiles[0])
        tmp = [[0 for r in range(nRows)] for c in range(nCols)]
        for r in range(nCols):
            for c in range(nRows):
                tmp[r][c] = tiles[c][r]
        return tmp

    @staticmethod
    def remove_empty(tiles):
        tmp = [[col for col in row if col>=0] for row in tiles]
        tmp = [row for row in tmp if len(row)>0]
        return tmp



