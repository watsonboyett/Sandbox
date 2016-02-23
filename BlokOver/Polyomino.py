from Piece import Piece
import math

class Polyomino:

    tiles = []

    mono_1 = [[1]]
   
    domo_1 = [[1,2],[-1,-1]]

    tromo_1 = [[1,2,3],[-1,-1,-1],[-1,-1,-1]]
    tromo_2 = [[1,2,-1],[3,0,-1],[-1,-1,-1]]
    #tromo_2a = [[1,2,-1],[3,0,-1],[-1,-1,-1]]

    tetro_1 = [[1,2,3,4],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    tetro_2 = [[1,2,-1,-1],[3,4,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    tetro_3 = [[1,2,3,-1],[0,4,0,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    tetro_4 = [[1,0,0,-1],[2,3,0,-1],[0,4,0,-1],[-1,-1,-1,-1]]
    tetro_5 = [[1,2,3,-1],[4,0,0,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    
    pento_1 = [[1,2,3,4,5],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_2 = [[0,1,2,-1,-1],[3,4,0,-1,-1],[0,5,0,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_3 = [[1,2,3,4,-1],[5,0,0,0,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_4 = [[1,2,3,-1,-1],[4,5,0,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_5 = [[1,2,3,0,-1],[0,0,4,5,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_6 = [[1,2,3,-1,-1],[0,4,0,-1,-1],[0,5,0,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_7 = [[1,2,3,-1,-1],[4,0,5,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_8 = [[1,2,3,-1,-1],[4,0,0,-1,-1],[5,0,0,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_9 = [[1,0,0,-1,-1],[2,3,0,-1,-1],[0,4,5,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_10 = [[0,1,0,-1,-1],[2,3,4,-1,-1],[0,5,0,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_11 = [[1,2,3,4,-1],[0,5,0,0,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    pento_12 = [[1,2,0,-1,-1],[0,3,0,-1,-1],[0,4,5,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    
    
    def __init__(self):
        pass

    def get_pieces(self,n):
        if n == 1:
            return [self.mono_1]
        elif n == 2:
            return [self.domo_1]
        elif n == 3:
            return [self.tromo_1,self.tromo_2]
        elif n == 4:
            return [self.tetro_1,self.tetro_2,self.tetro_3,self.tetro_4,self.tetro_5]
        elif n == 5:
            return [self.pento_1,self.pento_2,self.pento_3,self.pento_4,
                self.pento_5,self.pento_6,self.pento_7,self.pento_8,
                self.pento_9,self.pento_10,self.pento_11,self.pento_12]
    
    def num_free(self,n):
        if n == 1:
            return 1
        elif n == 2:
            return 1
        elif n == 3:
            return 2
        elif n == 4:
            return 5
        elif n == 5:
            return 12
    
    def check_free(self):
        # loop through each n-omino
        for ord_c in range(1,6):
            # get free pieces

            ominoes = self.get_pieces(ord_c)
            # loop through each piece
            for piece_i in range(len(ominoes)):
                piece = ominoes[piece_i]
                piece = [[int(math.ceil(float(col)/10)) for col in row] for row in piece]
                piece = Piece.remove_empty(piece)
                
                # check given piece against all other pieces
                for check_i in range(len(ominoes)):
                    # skip, if piece index is same as check index
                    if piece_i==check_i:
                        continue

                    # loop through all possible configurations (rotations/translations)
                    confs = range(0,8)
                    for conf_i in confs:
                        
                        # grab piece to check against
                        check = ominoes[check_i]
                        check = [[int(math.ceil(float(col)/10)) for col in row] for row in check]
                        check = Piece.remove_empty(check)
                        
                        if conf_i==0:
                            pass
                        elif conf_i==1:
                            check = Piece.rot_90(check)
                        elif conf_i==2:
                            check = Piece.rot_180(check)
                        elif conf_i==3:
                            check = Piece.rot_270(check)
                        elif conf_i==4:
                            check = Piece.mirror_horz(check)
                        elif conf_i==5:
                            check = Piece.mirror_horz(check)
                            check = Piece.rot_90(check)
                        elif conf_i==6:
                            check = Piece.mirror_vert(check)
                        elif conf_i==7:
                            check = Piece.mirror_vert(check)
                            check = Piece.rot_90(check)
                            
                        if piece==check:
                            print 'identical pieces found. {0},{1},{2},{3}'.format(
                                ord_c,piece_i,check_i,conf_i)
                            print piece
                            print check
                
        