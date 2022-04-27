class King:
    def __init__(self, team):
        self.team = team  # since we are using fen -> we are going by caps and no caps

        if self.team.isupper():
            self.image = 'Chess_klt60.bmp'
        else:
            self.image = 'Chess_kdt60.bmp'

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
        return []

    def __str__(self):
        if self.team.isupper():
            return 'K'
        else:
            return 'k'