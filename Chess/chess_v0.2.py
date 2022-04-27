import pygame
import os

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
        self.createBoard()
    
    def createBoard(self):
        width = self.surface.get_width() // 8
        height = self.surface.get_height() // 8
        
        temp = 1
        for rowIndex in range(8):
            row = []
            for colIndex in range(8):
                x = colIndex * width
                y = rowIndex * height
                if temp % 2 == 0:
                    color = '#769656'
                else:
                    color = '#eeeed2'
                tile = Tile(color, Piece(self.initBoard[rowIndex][colIndex]), x, y, width, height, self.surface)
                row.append(tile)
                temp += 1
            self.board.append(row)
            temp += 1
    
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
    
    def draw(self):
        self.surface.fill(self.bgColor)
        for row in self.board:
            for tile in row:
                tile.draw()
        pygame.display.update()
    
    def update(self):
        pass

    def decideContinue(self):
        pass


class Tile:
    def __init__(self, color, piece, x, y, width, height, surface):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.color = pygame.Color(color)
        self.piece = piece
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.piece.getImage() != None:
            self.surface.blit(pygame.image.load(self.piece.getImage()), self.rect)
        else:
            self.surface.fill(self.color, self.rect)

class Piece:
    def __init__(self, rank):
        pieces = {  'BRook': 5, 'BKnight': 3, 'BBishop': 3, 'BQueen': 9, 'BKing': 10, 'BPawn': 1,
                    'WRook': 5, 'WKnight': 3, 'WBishop': 3, 'WQueen': 9, 'WKing': 10, 'WPawn': 1, 'Blank': 0}
        path = './pieces/'
        images = {  'BRook': 'Chess_rdt60.bmp', 'BKnight': 'Chess_ndt60.bmp', 'BBishop': 'Chess_bdt60.bmp', 'BQueen': 'Chess_qdt60.bmp', 'BKing':'Chess_kdt60.bmp', 'BPawn': 'Chess_pdt60.bmp',
                    'WRook': 'Chess_rlt60.bmp', 'WKnight': 'Chess_nlt60.bmp', 'WBishop': 'Chess_blt60.bmp', 'WQueen': 'Chess_qlt60.bmp', 'WKing': 'Chess_klt60.bmp', 'WPawn': 'Chess_plt60.bmp', 'Blank': None}
        self.rank = pieces[rank]
        self.image = images[rank]
    
    def getImage(self):
        return self.image


main()