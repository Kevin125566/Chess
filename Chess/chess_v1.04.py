import pygame
import os
# This version has the working board being drawn

def main():
    pygame.init()
    pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Chess')
    wSurface = pygame.display.get_surface()
    game = Game(wSurface)
    game.play()
    pygame.quit()

class Game:
    def __init__(self, surface):
        # Initailizing the game surface
        self.surface = surface
        self.bgColor = pygame.Color('black')

        self.FPS = 60
        self.closeClicked = False
        self.continueGame = True

        self.initBoard = [  ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
                            ['BPawn']*8,
                            ['Blank']*8,
                            ['Blank']*8,
                            ['Blank']*8,
                            ['Blank']*8,
                            ['WPawn']*8,
                            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']]
        self.board = []
        # Initialize the board
        self.createBoard()

        self.tile = None
        self.otherTile = None
        self.validMoves = None
    
    def createBoard(self):
        # Getting the size of each square for our board
        width = self.surface.get_width() // 8
        height = self.surface.get_height() // 8
        
        # Initializing our board with the tiles which have the pieces in them
        temp = 1
        for rowIndex in range(8):
            row = []
            for colIndex in range(8):
                x = colIndex * width
                y = rowIndex * height
                if temp % 2 == 0:  # Alternating colors
                    color = '#769656'
                else:
                    color = '#eeeed2'
                if rowIndex == 0 or rowIndex == 1:  # Helps decide which color the pieces are
                    piece = Piece(self.initBoard[rowIndex][colIndex], 1)
                elif rowIndex == 6 or rowIndex == 7:
                    piece = Piece(self.initBoard[rowIndex][colIndex], 0)
                else:
                    piece = None
                tile = Tile(color, piece, x, y, width, height, self.surface)  # Creating our tile object
                row.append(tile)
                temp += 1
            self.board.append(row)
            temp += 1  # Add 1 at the end to have different color scheme for each row
    
    def play(self):
        while not self.closeClicked:
            self.handleEvents()
            self.draw()
            if self.continueGame:
                self.update()
                self.decideContinue()
    
    def handleEvents(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.closeClicked = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.continueGame:
                mousePos = pygame.mouse.get_pos()
                self.handleMouseEvents(mousePos)
            elif event.type == pygame.MOUSEBUTTONUP and self.continueGame:
                mousePos = pygame.mouse.get_pos()

    def handleMouseEvents(self, mousePos):
        for row in self.board:
            for tile in row:
                if tile.pressed(mousePos): 
                    if self.tile == None and tile.getPiece() != None:
                        self.tile = tile
                        print('hi')
                        self.validMoves = self.generateMoves()
                        self.tile.changeClicked()
                    elif self.tile != None:
                        self.otherTile = tile
                        self.otherTile.changeClicked()
                    if self.tile == self.otherTile:
                        self.validMoves = None
                        self.tile = None
                        self.otherTile = None
                    if self.tile != None and self.otherTile != None:
                        if self.otherTile in self.validMoves:
                            print(self.index_2d(self.tile))
                            print(self.index_2d(self.otherTile))
                            self.tile.moveTo(self.otherTile)
                            self.tile.changeClicked()
                            self.otherTile.changeClicked()
                            self.tile = None
                            self.otherTile = None
                            self.validMoves = None
    
    def index_2d(self, item):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == item:
                    return (row, col)
                            
    def draw(self):
        self.surface.fill(self.bgColor)
        # Drawing the tiles
        
        for row in self.board:
            for tile in row:
                tile.draw()
        if self.validMoves != None:
            print('asdasdas')
            for item in self.validMoves:
                item.draw(self.validMoves)        
        pygame.display.update()  # Do this to update the surface with our drawn tiles
    
    def update(self):
        pass

    def decideContinue(self):
        pass

    def rules(self, other):
        indexTile = self.index_2d(self.tile)
        indexOther = self.index_2d(other)
        rank = self.tile.getPiece().getRank()
        moves = self.tile.getPiece().getMoves()
        if rank == 'r' or rank == 'R':  # rook legal moves
            if indexTile[0] == indexOther[0]:  # other tile is in a different column
                diff = indexTile[1] - indexOther[1]
                if diff > 0:
                    step = -1
                elif diff < 0:
                    step = 1
                else:
                    return False
                # iterating through the columns in the same row to see if there is anything blocking the piece
                for col in range(indexTile[1] + step, indexOther[1], step):
                    if self.board[indexTile[0]][col].getPiece() != None:
                        return False
                return True
            elif indexTile[1] == indexOther[1]:  # other tile is in a different row
                diff = indexTile[0] - indexOther[0]
                if diff > 0:
                    step = -1
                elif diff < 0:
                    step = 1
                else:
                    return False
                # iterating through the rows in the same column to see if there is anything blocking the piece
                for row in range(indexTile[0] + step, indexOther[0], step):
                    if self.board[row][indexTile[1]].getPiece() != None:
                        return False
                return True
        elif rank == 'p' or rank == 'P':  # pawn legal moves
            diff = indexTile[0] - indexOther[0]
            if rank == 'p':
                if indexTile[1] == indexOther[1] and self.board[indexOther[0]][indexOther[1]].getPiece() == None:
                    if moves == 0 and diff == -2:
                        return True
                    elif diff == -1:
                        return True
            elif rank == 'P':
                if indexTile[1] == indexOther[1] and self.board[indexOther[0]][indexOther[1]].getPiece() == None:
                    if moves == 0 and diff == 2:
                        return True
                    elif diff == 1:
                        return True
            return False
        elif rank == 'n' or rank == 'N':
            offset = [(1, 2), (2, 1)]
            diff = (abs(indexTile[0] - indexOther[0]), abs(indexTile[1] - indexOther[1]))
            if diff in offset:
                return True
            return False
        elif rank == 'b' or rank == 'B':
            if abs(indexTile[1] - indexOther[1]) == abs(indexTile[0] - indexOther[0]):
                diff = indexTile[1] - indexOther[1]
                if diff > 0:
                    step = 1
                else:
                    step = -1 
                
                for i in range(indexTile[1], 8 - indexTile[0]):
                    if self.board[indexTile[0] + i][indexTile[1] + i] != None:
                        return False
                return True
            else:
                return False
            
            

        print('here')    
    def generateMoves(self):
        validMoves = []
        for row in self.board:
            for tile in row:
                if self.rules(tile):
                    validMoves.append(tile)
        return validMoves



class Tile:
    def __init__(self, color, piece, x, y, width, height, surface):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.origColor = pygame.Color(color)
        self.piece = piece
        self.isClicked = False
        
    
    def draw(self, validMoves = None):
        if validMoves != None:
            self.color = pygame.Color('#f44336')
        elif self.isClicked and self.piece != None:
            self.color = pygame.Color('#ffe9c5')
        else:
            self.color = self.origColor
        
        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.piece != None and self.piece.getImage() != None:
            self.surface.blit(pygame.image.load(self.piece.getImage()), self.rect)
        else:
            self.surface.fill(self.color, self.rect)
    
    def changeClicked(self):
        if self.isClicked and self.piece != None:
            self.isClicked = False
        else:
            self.isClicked = True
    
    def getClicked(self):
        return self.isClicked

    def pressed(self, pos):
        return pygame.Rect.collidepoint(self.rect, pos)

    def moveTo(self, other):
        if other.getPiece() == None or self.piece.getColor() != other.piece.getColor():
            self.piece.increment()
            other.changePiece(self.piece)
            self.piece = None

    def getPiece(self):
        return self.piece
    
    def changePiece(self, piece):
        self.piece = piece



class Piece:
    def __init__(self, rank, color):
        pieces = {  'BRook': 'r', 'BKnight': 'n', 'BBishop': 'b', 'BQueen': 'q', 'BKing': 'k', 'BPawn': 'p',
                    'WRook': 'R', 'WKnight': 'N', 'WBishop': 'B', 'WQueen': 'Q', 'WKing': 'K', 'WPawn': 'P', 'Blank': 0}

        images = {  'BRook': 'Chess_rdt60.bmp', 'BKnight': 'Chess_ndt60.bmp', 'BBishop': 'Chess_bdt60.bmp', 'BQueen': 'Chess_qdt60.bmp', 'BKing':'Chess_kdt60.bmp', 'BPawn': 'Chess_pdt60.bmp',
                    'WRook': 'Chess_rlt60.bmp', 'WKnight': 'Chess_nlt60.bmp', 'WBishop': 'Chess_blt60.bmp', 'WQueen': 'Chess_qlt60.bmp', 'WKing': 'Chess_klt60.bmp', 'WPawn': 'Chess_plt60.bmp', 'Blank': None}
        self.rank = pieces[rank]
        self.image = images[rank]
        self.color = color
        self.moves = 0
    
    def getImage(self):
        return self.image
    
    def getMoves(self):
        return self.moves

    def getRank(self):
        return self.rank
    
    def changeImage(self, image):
        self.image = image
    
    def changeRank(self, rank):
        self.rank = rank
    
    def getColor(self):
        return self.color

    def increment(self):
        self.moves += 1
    

main()