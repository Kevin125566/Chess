class Knight:  
    def __init__(self, team):
        self.team = team  # since we are using fen -> we are going by caps and no caps
        self.kingCheck = False

        if self.team.isupper():
            self.image = 'Chess_nlt60.bmp'
        else:
            self.image = 'Chess_ndt60.bmp'

    def getImage(self):
        return self.image
    
    def isSameTeam(self, otherPiece):
        '''
        Takes team from other piece and returns true if on the same team,
        false otherwise.

        Parameters: otherTeam -> str
        Return: bool
        '''
        # Check if the two pieces are on the same team
        if self.team != None:  # No piece on tile

            # Lower case for black, upper case for white
            otherTeam = otherPiece.getTeam()
            if self.team.islower() and otherTeam.islower():
                return True
            elif self.team.isupper() and otherTeam.isupper():
                return True

        return False
    
    def getTeam(self):
        '''
        This function returns the team of the piece

        Parameters: None
        Return: team -> str
        '''
        return self.team
    
    def getValidMoves(self, pos, board):
        '''
        This function gets the valid moves of the piece relative to its
        position

        Parameters: pos -> tuple (int, int)
        Return: moves -> list
        '''
        moves = []

        # The potential moves of the knight
        potential = [(-2, -1), (-2, 1), (2, -1), (2,1), (-1, -2), (-1, 2), (1, -2), (1, 2)]

        # Add the board to a dictionary so we don't have to do multiple lookups
        tiles = {}
        for row in board:
            for tile in row:
                tiles[tile.getCoords()] = tile
        
        self.kingCheck = False

        # Add the potential moves with the position and check if it is within bounds of the board
        for coord in potential:
            move = (coord[0] + pos[0], coord[1] + pos[1])
            # If the move is within the bounds of the board
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                otherTile = tiles[move]
                otherPiece = otherTile.getPiece()
                if otherTile.isOccupied() and self.isSameTeam(otherPiece):
                    continue
                if otherTile.isOccupied() and not self.isSameTeam(otherPiece) and otherPiece.getTeam().lower() == "k":
                    self.kingCheck = True
                moves.append(move)
        
        return moves

    def __str__(self):
        if self.team.isupper():
            return 'N'
        else:
            return 'n'