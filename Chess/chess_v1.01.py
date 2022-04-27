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
                print(mousePos)

    def handleMouseEvents(self, mousePos):
        for row in self.board:
            for tile in row:
                if tile.pressed(mousePos):
                    if self.tile == None and tile.getPiece() != None:
                        self.tile = tile
                        self.tile.changeClicked()
                    elif self.tile != None:
                        self.otherTile = tile
                        self.otherTile.changeClicked()
                    if self.tile != None and self.otherTile != None:
                        self.tile.moveTo(self.otherTile)
                        self.tile.changeClicked()
                        self.otherTile.changeClicked()
                        self.tile = None
                        self.otherTile = None
                


                            
    def draw(self):
        self.surface.fill(self.bgColor)
        # Drawing the tiles
        for row in self.board:
            for tile in row:
                tile.draw()
        pygame.display.update()  # Do this to update the surface with our drawn tiles
    
    def update(self):
        pass

    def decideContinue(self):
        pass



class Tile:
    def __init__(self, color, piece, x, y, width, height, surface):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.origColor = pygame.Color(color)
        self.piece = piece
        self.isClicked = False
        
    
    def draw(self):
        if self.isClicked and self.piece != None:
            self.color = pygame.Color('#f44336')
        else:
            self.color = self.origColor
        
        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.piece != None and self.piece.getImage() != None:
            self.surface.blit(pygame.image.load(self.piece.getImage()), self.rect)
        else:
            self.surface.fill(self.color, self.rect)
    
    def changeClicked(self):
        if self.isClicked:
            self.isClicked = False
        else:
            self.isClicked = True
    
    def getClicked(self):
        return self.isClicked

    def pressed(self, pos):
        return pygame.Rect.collidepoint(self.rect, pos)

    def moveTo(self, other):
        if other.getPiece() == None or self.piece.getColor() != other.piece.getColor():
            other.changePiece(self.piece)
            self.piece = None

    
    def getPiece(self):
        return self.piece
    
    def changePiece(self, piece):
        self.piece = piece

class Piece:
    def __init__(self, rank, color):
        pieces = {  'BRook': 5, 'BKnight': 3, 'BBishop': 3, 'BQueen': 9, 'BKing': 10, 'BPawn': 1,
                    'WRook': 5, 'WKnight': 3, 'WBishop': 3, 'WQueen': 9, 'WKing': 10, 'WPawn': 1, 'Blank': 0}

        images = {  'BRook': 'Chess_rdt60.bmp', 'BKnight': 'Chess_ndt60.bmp', 'BBishop': 'Chess_bdt60.bmp', 'BQueen': 'Chess_qdt60.bmp', 'BKing':'Chess_kdt60.bmp', 'BPawn': 'Chess_pdt60.bmp',
                    'WRook': 'Chess_rlt60.bmp', 'WKnight': 'Chess_nlt60.bmp', 'WBishop': 'Chess_blt60.bmp', 'WQueen': 'Chess_qlt60.bmp', 'WKing': 'Chess_klt60.bmp', 'WPawn': 'Chess_plt60.bmp', 'Blank': None}
        self.rank = pieces[rank]
        self.image = images[rank]
        self.color = color
    
    def getImage(self):
        return self.image
    
    def getMoves(self):
        pass

    def getRank(self):
        return self.rank
    
    def changeImage(self, image):
        self.image = image
    
    def changeRank(self, rank):
        self.rank = rank
    
    def getColor(self):
        return self.color


main()