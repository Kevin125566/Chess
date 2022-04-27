import pygame
import os
import board as b
import time

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

        self.gameBoard = b.Board()
        self.board = []

        self.createBoard()

        self.tile = None
        self.otherTile = None

        self.moveHistory = []

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
                tile = BoardTile(color, self.gameBoard.getTile((rowIndex, colIndex)), x, y, width, height, self.surface)
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
                self.handleMouseEvents(mousePos)
            elif event.type == pygame.MOUSEBUTTONUP and self.continueGame:
                mousePos = pygame.mouse.get_pos()
                #print(mousePos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.undo()

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
                        #start = time.time()
                        self.moveHistory.append((self.tile, self.otherTile))
                        self.tile.changeClicked()
                        self.otherTile.changeClicked()
                        self.gameBoard.move(self.tile.getTile(), self.otherTile.getTile())
                        self.tile.updatePiece()
                        self.otherTile.updatePiece() 
                        self.tile = None
                        self.otherTile = None
                        #end = time.time()
                        #print("Time elapsed:", end - start)
    
    def draw(self):
        self.surface.fill(self.bgColor)

        validTile = False
        if self.tile != None:
            validTile = True
            tile = self.tile.getTile()
            coords = tile.getCoords()
            piece = tile.getPiece()
            moves = piece.getValidMoves(coords, self.gameBoard.board)

        for row in self.board:
            for tile in row:
                if validTile and tile.getTile().getCoords() in moves:
                    tile.draw(True)
                else:
                    tile.draw(False)
    
        pygame.display.update()
        #print(self.gameBoard)
    
    def undo(self):
        self.gameBoard.unMove()
        
        if len(self.moveHistory) != 0:
            tiles = self.moveHistory.pop()
            tile = tiles[0]
            otherTile = tiles[1]

            tile.updatePiece()
            otherTile.updatePiece()


    
    def update(self):
        pass

    def decideContinue(self):
        pass


class BoardTile:
    def __init__(self, color, tile, x, y, width, height, surface):
        self.tile = tile
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.origColor = pygame.Color(color)
        self.piece = tile.getPiece()
        self.isClicked = False
    
    def draw(self, highlight):
        
        if highlight:
            if self.origColor == pygame.Color('#769656'):
                self.color = pygame.Color('#f44336')
            else:
                self.color = pygame.Color('#f66055')
        elif self.isClicked and self.piece != None:
                self.color = pygame.Color('#ffe9c5')
        else:
            self.color = self.origColor

        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.tile.isOccupied():
            self.surface.blit(pygame.image.load(self.tile.getPiece().getImage()), self.rect)
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
    
    def getPiece(self):
        return self.piece
    
    def getTile(self):
        return self.tile

    def updatePiece(self):
        self.piece = self.tile.getPiece()


main()