class Rook:
    def __init__(self, team):
        self.team = team  # since we are using fen -> we are going by caps and no caps

        if self.team.isupper():
            self.image = 'Chess_rlt60.bmp'
        else:
            self.image = 'Chess_rdt60.bmp'

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

        # All the potential moves of the rook
        rookPotMovesDown = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        rookPotMovesUp = [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]
        rookPotMovesRight = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        rookPotMovesLeft = [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]

        # Add the board to a dictionary so we don't have to do multiple lookups
        tiles = {}
        for row in board:
            for tile in row:
                tiles[tile.getCoords()] = tile

        # Add the potential moves with the position and check if it is within bounds of the board
        for coord in rookPotMovesRight:
            move = (coord[0] + pos[0], coord[1] + pos[1])
            # If the move is within the bounds of the board
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                otherTile = tiles[move]
                otherPiece = otherTile.getPiece()
                if otherTile.isOccupied() and self.isSameTeam(otherPiece):
                    break
                elif otherTile.isOccupied() and not self.isSameTeam(otherPiece):
                    moves.append(move)
                    break
                moves.append(move)
        
        for coord in rookPotMovesDown:
            move = (coord[0] + pos[0], coord[1] + pos[1])
            # If the move is within the bounds of the board
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                otherTile = tiles[move]
                otherPiece = otherTile.getPiece()
                if otherTile.isOccupied() and self.isSameTeam(otherPiece):
                    break
                elif otherTile.isOccupied() and not self.isSameTeam(otherPiece):
                    moves.append(move)
                    break
                moves.append(move)
        
        for coord in rookPotMovesLeft:
            move = (coord[0] + pos[0], coord[1] + pos[1])
            # If the move is within the bounds of the board
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                otherTile = tiles[move]
                otherPiece = otherTile.getPiece()
                if otherTile.isOccupied() and self.isSameTeam(otherPiece):
                    break
                elif otherTile.isOccupied() and not self.isSameTeam(otherPiece):
                    moves.append(move)
                    break
                moves.append(move)
        
        for coord in rookPotMovesUp:
            move = (coord[0] + pos[0], coord[1] + pos[1])
            # If the move is within the bounds of the board
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                otherTile = tiles[move]
                otherPiece = otherTile.getPiece()
                if otherTile.isOccupied() and self.isSameTeam(otherPiece):
                    break
                elif otherTile.isOccupied() and not self.isSameTeam(otherPiece):
                    moves.append(move)
                    break
                moves.append(move)

        return moves

    def __str__(self):
        if self.team.isupper():
            return 'R'
        else:
            return 'r'