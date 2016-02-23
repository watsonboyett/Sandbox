

class Blokus:

    board = []
    cover = []

    def __init__(self,Board):
        self.board = Board


    

    def can_add(self,Piece):
        # check if any piece tiles are already used on the board
        isect = filter(set(Piece.cover).__contains__,self.cover)
        if any(isect):
            return False
        
        # current piece does not overlap any others on the board
        return True
    
    
    def add_piece(self,Piece):
        # add given piece to the board
        self.cover = self.cover + Piece.cover
    
    
    
    

    def dfs_edges(G,source=None):
        """Produce edges in a depth-first-search starting at source."""
        # Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
        # by D. Eppstein, July 2004.
        if source is None:
            # produce edges for all components
            nodes=G
        else:
            # produce edges for components with source
            nodes=[source]
        visited=set()
        for start in nodes:
            if start in visited:
                continue
            visited.add(start)
            stack = [(start,iter(G[start]))]
            while stack:
                parent,children = stack[-1]
                try:
                    child = next(children)
                    if child not in visited:
                        yield parent,child
                        visited.add(child)
                        stack.append((child,iter(G[child])))
                except StopIteration:
                    stack.pop()
