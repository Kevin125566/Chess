class Pawn:
    def __init__(self, team):
        self.team = team  # since we are using fen -> we are going by caps and no caps
        self.enPassant = True  # The pawn can move 2 spaces forward
        self.kingCheck = False

        if self.team.isupper():
            self.image = 'Chess_plt60.bmp'
        else:
            self.image = 'Chess_pdt60.bmp'

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
    
    def canEnPassant(self):
        '''
        This function returns whether the pawn can en passant

        Parameters: None
        Return: enPassant -> boolean
        '''
        return self.enPassant
    
    def removeEnPassant(self):
        '''
        This function removes the pawns ability to en passant

        Parameters: None
        Return: None
        '''
        self.enPassant = False
    
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

        # Potential moves for the pawn pieces --> different for different teams
        blackPotMoves = [(1, 0)]
        blackPotTakes = [(1, -1), (1, 1)]
        whitePotMoves = [(-1, 0)]
        whitePotTakes = [(-1, -1), (-1, 1)]

        if self.team == "p" and self.enPassant:
            blackPotMoves.append((2, 0))
        elif self.team == "P" and self.enPassant:
            whitePotMoves.append((-2, 0))

        # Add the board to a dictionary so we don't have to do multiple lookups
        tiles = {}
        for row in board:
            for tile in row:
                tiles[tile.getCoords()] = tile

        # Add the potential moves with the position and check if it is within bounds of the board
        if self.team.isupper():
            for coord in whitePotMoves:
                move = (coord[0] + pos[0], coord[1] + pos[1])
                # If the move is within the bounds of the board
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    otherTile = tiles[move]
                    otherPiece = otherTile.getPiece()
                    if otherTile.isOccupied():  # If there is a piece in front of it
                        break
                    moves.append(move)
            
            for coord in whitePotTakes:
                move = (coord[0] + pos[0], coord[1] + pos[1])
                # If the move is within the bounds of the board
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    otherTile = tiles[move]
                    otherPiece = otherTile.getPiece()
                    if otherTile.isOccupied() and self.isSameTeam(otherPiece):  # Pawn can potentially take if not same team
                        continue
                    elif not otherTile.isOccupied():  # There is no take available
                        continue
                    moves.append(move)
        else:
            # Add the potential moves with the position and check if it is within bounds of the board
            for coord in blackPotMoves:
                move = (coord[0] + pos[0], coord[1] + pos[1])
                # If the move is within the bounds of the board
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    otherTile = tiles[move]
                    otherPiece = otherTile.getPiece()
                    if otherTile.isOccupied():
                        break
                    moves.append(move)
            
            for coord in blackPotTakes:
                move = (coord[0] + pos[0], coord[1] + pos[1])
                # If the move is within the bounds of the board
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    otherTile = tiles[move]
                    otherPiece = otherTile.getPiece()
                    if otherTile.isOccupied() and self.isSameTeam(otherPiece):  # Pawn can potentially take if not same team
                        continue
                    elif not otherTile.isOccupied():  # There is no take available
                        continue
                    moves.append(move)
        
        return moves

    def __str__(self):
        if self.team.isupper():
            return 'P'
        else:
            return 'p'
