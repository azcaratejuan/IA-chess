import ChessAlgoritmo
import pygame as p
import math


ancho = alto = 400
dim = 8 
sqsize = alto // dim
frames = 10
images = {} 

def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece +".png"),(sqsize,sqsize))
        
def main():
    p.init()
    screen = p.display.set_mode((ancho,alto))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))

    gs = ChessAlgoritmo.Estado()
    validMoves = gs.getJugadasV()
    moveMade = False
    loadImages()
    running = True
    
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN and gs.blancasTurno:
                location = p.mouse.get_pos()
                col = location[0]//sqsize
                row = location[1]//sqsize
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                    
                if len(playerClicks) == 2:
                    move = ChessAlgoritmo.Move(playerClicks[0],playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.HacerMovimiento(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            
                    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getJugadasV()
            moveMade = False
        drawEstado(screen, gs)
        clock.tick(frames)
        p.display.flip()

        if gs.mate and not gs.AIturn:
            print("Ganan las negras") if gs.whiteToMove else print("Ganan las blancas")
            running = False
        
        if gs.tablas and not gs.AIturn:
            print("tablas")
            running = False

        if not gs.blancasTurno and len(validMoves) != 0 and not moveMade:
            x = gs.Mejorjugada(2, False)
            gs.HacerMovimiento(x)
            moveMade = True
            

def drawEstado(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colours = [p.Color("white"),p.Color("black")]
    for r in range(dim):
        for c in range(dim):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))
            
            

def drawPieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))




if __name__ == "__main__":
    main()
