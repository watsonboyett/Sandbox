
class Board:

    nRows = 10
    nCols = 10
    board = []

    def __init__(self,nRows,nCols):
        self.nRows = nRows
        self.nCols = nCols
    
    def build_ids(self):
        board = [ x+y+1 for x in range(0,self.nRows*self.nCols,self.nCols) 
            for y in range(self.nCols) ]

        self.board = board

    def build_ids2(self):
        board = [ [x+y+1 for x in range(self.nCols) ]
            for y in range(0,self.nCols*self.nRows,self.nCols) ]
        self.board = board

    def get_cover(self,piece):
        tiles = piece.tiles
        nVert = len(tiles)
        nHorz = len(tiles[0])
        
        # check if tile fits vertically
        if (piece.pos[0] + nVert) > self.nRows:
            return []
        
        # check if tile fits horizontally
        if (piece.pos[1] + nHorz) > self.nCols:
            return []

        # get ids
        ids = []
        for v in range(nVert):
            for h in range(nHorz):
                if tiles[v][h]>0:
                    r = piece.pos[0] + v
                    c = piece.pos[1] + h
                    ids.append(self.board[r][c])

        return ids



