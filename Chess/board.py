from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook

class Tile:
    def __init__(self, coords, piece):
        self.piece = piece
        self.coords = coords

        # If self.piece is None then there is no piece on the tile
        if self.piece != None:
            self.containsPiece = True
        else:
            self.containsPiece = False
    
    def setPiece(self, piece):
        self.piece = piece

        if self.piece != None:
            self.containsPiece = True
        else:
            self.containsPiece = False
    
    def getCoords(self):
        return self.coords
    
    def getPiece(self):
        return self.piece
    
    def isOccupied(self):
        return self.containsPiece
    
    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return " "

class Board:
    def __init__(self):
        self.fenCurrent = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" # "w KQkq - 0 1" -> w means white moves next - means no castling available

        # The structure for creating the actual board where the tiles and pieces are
        self.initBoard=[['r','n','b','q','k','b','n','r'],
                        ['p','p','p','p','p','p','p','p'],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        ['P','P','P','P','P','P','P','P'],
                        ['R','N','B','Q','K','B','N','R']]
        
        # The initial starting board positions -> updated every move
        self.board = []
        self.moveHistory = []  # will be a tuple containing last pos of black and white -> (white, whiteCoord, black, blackCoord)

        pieces={'r': Rook('r'), 'n': Knight('n'), 'b': Bishop('b'), 'q': Queen('q'), 'k': King('k'), 'p': Pawn('p'),
                'R': Rook('R'), 'N': Knight('N'), 'B': Bishop('B'), 'Q': Queen('Q'), 'K': King('K'), 'P': Pawn('P')}

        for x in range(len(self.initBoard)):
            row = []  # Create the row for the tilesS
            for y in range(len(self.initBoard)):
                tile = self.initBoard[x][y]
                if tile == "r":
                    piece = Rook('r')
                elif tile == 'n':
                    piece = Knight('n')
                elif tile == 'b':
                    piece = Bishop('b')
                elif tile == 'q':
                    piece = Queen('q')
                elif tile == 'k':
                    piece = King('k')
                elif tile == 'p':
                    piece = Pawn('p')
                elif tile == "R":
                    piece = Rook('R')
                elif tile == 'N':
                    piece = Knight('N')
                elif tile == 'B':
                    piece = Bishop('B')
                elif tile == 'Q':
                    piece = Queen('Q')
                elif tile == 'K':
                    piece = King('K')
                elif tile == 'P':
                    piece = Pawn('P')
                else:
                    piece = None
                #piece = pieces.get(self.initBoard[x][y], None)  # Get the pieces from the dictionary, if not exist return None
                tile = Tile((x, y), piece)  # Create the tile with the coords and piece in it
                row.append(tile)
            self.board.append(row)
        
        # TODO: - Create a coordinate system on the board for the fen structure
        #       - Create the movesNext method that determines who gets to move next
        #           - fen structure will use movesNext for its string
        #       - Create a method that will determine where the piece has moved Ex: Pb1 to b3
        #       - For some reason en passant removes it for all pawns of same team -> gotta fix

        
    def generateFen(self):
        '''
        Generates a new fen structure for the board

        Parameters: None
        Return: None
        '''

        fen = ""
        spaces = 0
        for row in self.board:
            for tile in row:
                if tile == " ":
                    spaces += 1
                else:
                    if spaces != 0:
                        fen += str(spaces)
                        spaces = 0
                    fen += str(tile)
            if spaces != 0:
                fen += str(spaces)
                spaces = 0
            fen += '/'
        
        self.fenCurrent = fen[:-1]
        

    def isValidMove(self, tile, moveTo):
        '''
        This function gets all the valid moves of the piece and
        checks if the move is in those valid moves

        Parameters: tile -> Object, moveTo -> tuple (x, y)
        Return: bool
        '''
        # Get the valid moves of the coords of the tile
        coords = tile.getCoords()
        piece = tile.getPiece()
        
        # The selected tile has no piece on it
        if not piece:
            return False
    
        moves = piece.getValidMoves(coords, self.board)
        
        otherCoords = moveTo.getCoords()
        occupied = moveTo.isOccupied()

        # If the coords of moveTo are in moves and the moveTo piece is not on the same team
        if otherCoords in moves:
            if not occupied:  # If the tile has no pieces
                if piece.getTeam() == "P" or piece.getTeam() == "p":
                    # The piece is a pawn so they can't enpassant anymore
                    piece.removeEnPassant()
                return True
            elif not piece.isSameTeam(moveTo.getPiece()):  # If the two pieces are not on the same team
                if piece.getTeam() == "P" or piece.getTeam() == "p":
                    # The piece is a pawn so they can't enpassant anymore
                    piece.removeEnPassant()
                return True
        
        return False
    
    def getTile(self, coord):
        '''
        This function iterates through the board and finds the tile of the same
        coordinates, if not found return None

        Parameters: coord -> tuple
        Return: tile -> Object
        '''
        for row in self.board:
            for tile in row:
                x, y = tile.getCoords()
                if x == coord[0] and y == coord[1]:
                    return tile
        
        return None

    def move(self, tile1, tile2):
        '''
        This function moves the piece to the tile if it is valid

        Parameters: tile1 -> Object, tile2 -> Object
        Return: None
        '''
        if self.isValidMove(tile1, tile2):
            self.moveHistory.append((tile1.getPiece(), tile1.getCoords(), tile2.getPiece(), tile2.getCoords()))  # Record move so we can undo it

            tile2.setPiece(tile1.getPiece())
            tile1.setPiece(None)
            tile2.getPiece().getValidMoves(tile2.getCoords(), self.board)  # This is called to get see if the move results in a check

    def unMove(self):
        '''
        This function reverts the previous move

        Parameters: None
        Return: None
        '''
        if len(self.moveHistory) == 0:
            print("There is no move to undo")
        else:
            move = self.moveHistory.pop()
            white = move[0]
            whiteTile = self.getTile(move[1])
            black = move[2]
            blackTile = self.getTile(move[3])

            whiteTile.setPiece(white)
            blackTile.setPiece(black)

    def movesNext(self):
        '''
        This function determines whether white or black gets to move

        Parameters:
        Return:
        '''
        pass

    def __repr__(self):
        '''
        Creates a string representation of the current board position
        Parameter: None
        Return: myStr -> str
        '''
        myStr = ''
        for row in self.board:
            myStr += '| '
            for tile in row:
                myStr += str(tile) + ' | '
            myStr += '\n'
        
        return myStr


def main():
    board = Board()
    print(board)
    print("\nMoving knight to legal space\n")
    board.move(board.getTile((7,1)), board.getTile((5,2)))  # This move sohuld be legal
    print(board)
    print("\nMoving knight to legal space\n")
    board.move(board.getTile((5,2)), board.getTile((3,1)))  # This move should be legal
    print(board)
    print("\nMoving knight to legal space\n")
    board.move(board.getTile((3,1)), board.getTile((1,2)))  # This move should be legal
    print(board.getTile((3,1)).isOccupied())
    print(board)
    print("\nMoving bishop to illegal space\n")
    board.move(board.getTile((7,2)), board.getTile((5,1)))  # This move should be illegal
    print(board)
    print("\nMoving biship to illegal space\n")
    board.move(board.getTile((7,2)), board.getTile((5,4)))  # This move should be illegal --> but its not we need to fix  -- UPDATE: fixed!!! :)
    print(board)


if __name__ == '__main__':
    main()