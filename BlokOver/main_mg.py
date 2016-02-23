
from Board import Board
from Polyomino import Polyomino
from Piece import Piece
from Blockus import Blockus

import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# board parameters
rows_n = 10
cols_n = 10

# piece parameters
ords = [1,2,3]
colors = [0,1,3]
confs = range(0,8)


# setup 2-D board of IDs
board = Board(rows_n,cols_n)
board.build_ids2()
#print board.board

# setup tiles
poly = Polyomino()
cands = []
id_i = 0

# loop through each set of n-ominoes
for ord_c in ords:

    # get pieces
    ominoes = poly.get_pieces(ord_c)

    # loop through each n-omino
    ominoes_n = len(ominoes)
    for omino_i in range(ominoes_n):

        # loop through each configuration
        for conf_i in confs:

            # skip configurations that aren't unique
            if ord_c<=1 and conf_i>=1:
                continue
            if ord_c<=2 and conf_i>=2:
                continue
            if ord_c<=3 and conf_i>=4:
                continue

            # get current piece & remove empty rows/cols
            tiles = ominoes[omino_i];
            tiles = Piece.remove_empty(tiles)
            
            # rotate/mirror current piece
            if conf_i==0:
                pass
            elif conf_i==1:
                tiles = Piece.rot_90(tiles)
            elif conf_i==2:
                tiles = Piece.rot_180(tiles)
            elif conf_i==3:
                tiles = Piece.rot_270(tiles)
            elif conf_i==4:
                tiles = Piece.mirror_horz(tiles);
            elif conf_i==5:
                tiles = Piece.mirror_horz(tiles);
                tiles = Piece.rot_90(tiles)
            elif conf_i==6:
                tiles = Piece.mirror_vert(tiles);
            elif conf_i==7:
                tiles = Piece.mirror_vert(tiles);
                tiles = Piece.rot_90(tiles)


            # loop through each tile color
            for color_i in colors:

                # loop through each row
                for row_c in range(rows_n):

                    # loop through each column
                    for col_c in range(cols_n):

                        cPiece = Piece(tiles)
                        cPiece.order = ord_c
                        cPiece.key = omino_i
                        cPiece.conf = conf_i
                        cPiece.color = color_i
                        cPiece.pos = [row_c,col_c]

                        # get coverage
                        cPiece.cover = board.get_cover(cPiece)
                        cPiece.id = id_i
                        id_i = id_i + 1

                        cands.append(cPiece)
        print 'Order {0}, Piece {1}, Total: {2}'.format(ord_c,omino_i,len(cands))
print 'Completed Piece Layout: {0} pieces.\n'.format(len(cands))



# find all pieces that match the given criteria
def find_level(cands,ord,key,color):
    return [cand for cand in cands
            if (cand.order==ord and cand.key==key and cand.color==color)]

# build levels (one piece of one color of one order per level)
total = 0
lev_i = 0
levels = []
for ord_c in ords:
    for key_c in range(poly.num_free(ord_c)):
        for color_c in colors:
            level_cur = find_level(cands,ord_c,key_c,color_c)
            levels.append(level_cur)
            
            print 'Level {0} : order {1}, key {2}, color {3} : {4}'.format(lev_i,ord_c,key_c,color_c,len(level_cur))
            lev_i = lev_i + 1
            total = total + len(level_cur)
            
print 'Completed Level Building: {0} levels.\n'.format(len(levels))



# build graph of each level
blok = Blockus(board)
DG = nx.MultiDiGraph()
levels_n = len(levels)
for lev_i in range(levels_n-1):
    lev_cur = levels[lev_i]
    lev_nxt = levels[lev_i+1]

    src_n = len(lev_cur)
    tar_n = len(lev_nxt)
    for src_i in range(src_n):
        src = lev_cur[src_i]
        for tar_i in range(tar_n):
            tar = lev_nxt[tar_i]
                
            # determine if pieces can exist together, add edge if so
            if blok.can_place(src,tar):
                # ensure node exist before checking in-degree
                if src.id in DG:
                    in_degree = DG.in_degree(src.id)
                else:
                    in_degree = 0
                    
                if in_degree < 1:
                    # first level - no need to check previous coverage, just add source data
                    DG.add_edge(src.id,tar.id, weight=1, cover=src.cover, ids=src.id)
                else:
                    # must ensure target pieces don't collide with existing ones
                    for edge in DG.in_edges_iter(src.id):
                        # create new "piece" representing all tiles currently occupied
                        cnxs = DG.get_edge_data(*edge)
                        rem_list = []
                        for ci in cnxs:
                            cover = cnxs[ci]['cover']
                            ids = cnxs[ci]['ids']
                            tp = Piece([])
                            tp.cover = cover
    
                            # add target piece to occupied spaces
                            if blok.can_place(tp,tar):
                                rem_list.append(ci)
                                DG.add_edge(src.id,tar.id, weight=1, cover=tp.cover+tar.cover, ids=ids+tar.id)
                        
                        # remove old edges (to save memory)
                        for key in rem_list:
                            DG.remove_edge(*edge,key=key)    
    print 'Level {0} : Sources {1}, Targets {2}'.format(lev_i,src_n,tar_n)
print 'Completed Graph Layout: {0} nodes.\n'.format(len(DG))



# find paths through the graph
paths = []
for src_id in range(levels[0][0].id,levels[0][-1].id+1):
    for tar_id in range(levels[-1][0].id,levels[-1][-1].id+1):

        path_exist = nx.has_path(DG,src_id,tar_id)
        if path_exist:
            path_ids = nx.shortest_path(DG,src_id,tar_id)
            print 'found path from {0} to {1}'.format(src_id,tar_id)
            path = [cands[i] for i in path_ids]
            cover = [p.cover for p in path]
            print cover
            paths.append(path_ids)
            exit()
print 'Completed Path Mapping: {0} paths.\n'.format(len(paths))



# show the graph results
if False:
    nx.graph
    shells = [[p.id for p in lev] for lev in levels]
    pos = nx.shell_layout(DG,shells)
    nx.draw(DG,pos)
    plt.axis('equal')
    plt.show()
    
# show results


