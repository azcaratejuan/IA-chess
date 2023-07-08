import math
import copy


class Estado():
    def __init__(self):

        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions = {'P': self.MovimientosPeon, 'R': self.MovimientosTorre, 'N': self.MovimientosCaballo,
                              'B': self.MovimientoAlfil, 'Q': self.MovimientosReyna, 'K': self.MovimientosRey}
        
        #declaraciones inciales y donde se encuentra el rey de ambos lados
        self.wkingpos = (7,4)
        self.bkingpos = (0,4)        
        self.blancasTurno = True
        self.AIturn = False
        self.moveLog = []
        self.mate = False
        self.tablas = False
        self.capturar = ()
        
        #declaramos los enroques posibles 
        self.enroqueDerecho = enroque(True, True, True, True)
        self.enroqueHis = [enroque(self.enroqueDerecho.wks, self.enroqueDerecho.bks,
                                             self.enroqueDerecho.wqs, self.enroqueDerecho.bqs)]
        
        
  
    def HacerMovimiento(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.MoverPieza
        self.moveLog.append(move)
        self.blancasTurno = not self.blancasTurno

        if move.MoverPieza == 'wK':
            self.wkingpos = (move.endRow, move.endCol)
        elif move.MoverPieza == 'bK':
            self.bkingpos = (move.endRow, move.endCol)

        # peon a reina
        if move.promocion:
            self.board[move.endRow][move.endCol] = move.MoverPieza[0] + 'Q'

        # captura de peones
        if move.capturado:
            self.board[move.startRow][move.endCol] = '--'
        if move.MoverPieza[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.capturar = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.capturar = ()

        if move.movimientoTorre:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        
        self.actualizarEnroque(move)
        self.enroqueHis.append(enroque(self.enroqueDerecho.wks, self.enroqueDerecho.bks,
                                             self.enroqueDerecho.wqs, self.enroqueDerecho.bqs))

        
                

    def deshacer(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.MoverPieza
            self.board[move.endRow][move.endCol] = move.capturaMemori
            #turno
            self.blancasTurno = not self.blancasTurno
            # verificamos si fueron los retes parea los enroques
            if move.MoverPieza == 'wK':
                self.wkingpos = (move.startRow, move.startCol)
            elif move.MoverPieza == 'bK':
                self.bkingpos = (move.startRow, move.startCol)

            # devolvemos captura
            if move.capturado:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.capturaMemori
                self.capturar = (move.endRow, move.endCol)
            if move.MoverPieza[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.capturar = ()
                
            # devolvemos torres y verificamos por enroque
            if move.movimientoTorre:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
            
            self.enroqueHis.pop()
            self.enroqueDerecho = self.enroqueHis[-1]
            


    def actualizarEnroque(self, move):
        if move.MoverPieza == 'wK':
            self.enroqueDerecho.wks = False
            self.enroqueDerecho.wqs = False
        elif move.MoverPieza == 'bK':
            self.enroqueDerecho.bks = False
            self.enroqueDerecho.bqs = False
        elif move.MoverPieza == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.enroqueDerecho.wqs = False
                elif move.startCol == 7:
                    self.enroqueDerecho.wks = False

        elif move.MoverPieza == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.enroqueDerecho.bqs = False
                elif move.startCol == 7:
                    self.enroqueDerecho.bks = False
                

                

    def getJugadasV(self):
        capturarTemp = self.capturar
        tempEnroque = enroque(self.enroqueDerecho.wks, self.enroqueDerecho.bks,
                                        self.enroqueDerecho.wqs, self.enroqueDerecho.bqs)
        moves = self.ObtenerMovimientos()
        if self.blancasTurno:
            self.Movimientostorre(self.wkingpos[0], self.wkingpos[1], moves)
        else:
            self.Movimientostorre(self.bkingpos[0], self.bkingpos[1], moves)
        for i in range(len(moves)-1,-1,-1):
                # hacemos las jugadas y cambiamos turno
            self.HacerMovimiento(moves[i])
            self.blancasTurno = not self.blancasTurno
            if self.RevisionTurno():
                # eliminamos la jugada anterior
                moves.remove(moves[i])
                #devolvemos el turno
            self.blancasTurno = not self.blancasTurno
            self.deshacer()
            #revisamos que si hay mate o llegamos a punto muerto y pasamos a tablas
        if len(moves) == 0:
            # sees if in check or tablas
            if self.RevisionTurno():
                self.mate = True
            else:
                self.tablas = True
        
        #verificamos y devolvemos el movimiento posible
        self.capturar = capturarTemp
        self.enroqueDerecho = tempEnroque
        return moves

    def RevisionTurno(self):

        if self.blancasTurno:
            return self.Verificacionjugada(self.wkingpos[0], self.wkingpos[1])
        else:
            return self.Verificacionjugada(self.bkingpos[0], self.bkingpos[1])

    def Verificacionjugada(self, r, c):
        # vemos si la jugada es posible dentro de las posibilidades y devolvemos true en caso
        self.blancasTurno = not self.blancasTurno
        oppMoves = self.ObtenerMovimientos()
        self.blancasTurno = not self.blancasTurno
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False 


    def ObtenerMovimientos(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
              #vemos si es es black o white
                turn = self.board[r][c][0]
                if (turn == 'w' and self.blancasTurno) or (turn == 'b' and not self.blancasTurno):
                    # vemos que tipo de pieza es para saber que tipo de movimiento revisar
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves




                     
    def MovimientosPeon(self, r, c, moves):
        if self.blancasTurno:
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c - 1 >= 0: 
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.capturar:
                    moves.append(Move((r, c), (r-1, c-1), self.board, capturado = True))
            if c + 1 <= 7: 
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.capturar:
                    moves.append(Move((r, c), (r-1, c+1), self.board, capturado = True))

        else:
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c-1), self.board))
                elif (r + 1, c - 1) == self.capturar:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, capturado = True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r + 1, c + 1) == self.capturar:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, capturado = True))
        
    def MovimientosTorre(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        oppColour = 'b' if self.blancasTurno else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == oppColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
            
    def MovimientoAlfil(self, r, c, moves):
        directions = ((-1,-1), (1,-1), (1,1), (-1,1))
        oppColour = 'b' if self.blancasTurno else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == oppColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                
    def MovimientosReyna(self, r, c, moves):
        self.MovimientosTorre(r, c, moves)
        self.MovimientoAlfil(r, c, moves)

    def MovimientosCaballo(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColour = 'w' if self.blancasTurno else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def MovimientosRey(self, r, c, moves):
        directions = ((-1,-1), (1,-1), (1,1), (-1,1), (-1,0), (0,-1), (1,0), (0,1))
        allyColour = 'w' if self.blancasTurno else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    

    def Movimientostorre(self, r, c, moves):
        if self.Verificacionjugada(r, c):
            return
        if (self.blancasTurno and self.enroqueDerecho.wks) or (not self.blancasTurno and self.enroqueDerecho.bks):
            self.reyEnroque(r, c, moves)
        if (self.blancasTurno and self.enroqueDerecho.wqs) or (not self.blancasTurno and self.enroqueDerecho.bqs):
            self.ReynaEnroque(r, c, moves)

    def reyEnroque(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.Verificacionjugada(r, c + 1) and not self.Verificacionjugada(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, movimientoTorre = True))

    def ReynaEnroque(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.Verificacionjugada(r, c - 1) and not self.Verificacionjugada(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, movimientoTorre = True))


    def minimax(self, profundidad, alpha, beta, Max):
        possibleMoves = self.getJugadasV()
        value = self.MejoresJugadas()
        if profundidad == 0 or value == -math.inf or value == math.inf:
                return value
        if Max:
            maxEval = -math.inf
            for move in possibleMoves:
                self.HacerMovimiento(move)
                evaluation = self.minimax(profundidad - 1, alpha, beta, False)
                self.deshacer()
                if (evaluation > maxEval):
                    maxEval = evaluation
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = math.inf
            for move in possibleMoves:
                self.HacerMovimiento(move)
                evaluation = self.minimax(profundidad - 1, alpha, beta, True)
                self.deshacer()
                minEval = min(evaluation, minEval)
                beta = min(evaluation, beta)
                if beta <= alpha:
                    break
            return minEval
                         
    def Mejorjugada(self, profundidad, Max):
        mateTemp = copy.deepcopy(self.mate)
        tablasTemp = copy.deepcopy(self.tablas)
        torreTemp = copy.deepcopy((self.enroqueDerecho.wks, self.enroqueDerecho.bks,
                                             self.enroqueDerecho.wqs, self.enroqueDerecho.bqs))

        self.AIturn = True
        moves = self.getJugadasV()
        bestValue = -math.inf if Max else math.inf
        bestMove = None
        for move in moves:
            self.HacerMovimiento(move)
            value = self.minimax(profundidad - 1, -math.inf, math.inf, not Max)
            self.deshacer()
            if value == -math.inf and not Max:
                return move
            elif value == math.inf and Max:
                return move
            else:
                if Max:
                    try:
                        if value > bestValue:
                            bestValue = value
                            bestMove = copy.deepcopy(move)
                    except:
                        pass
                else:
                    try:
                        if value < bestValue:
                            bestValue = value
                            bestMove = copy.deepcopy(move)
                    except:
                        pass
        self.AIturn = False
        self.mate = copy.deepcopy(mateTemp)
        self.tablas = copy.deepcopy(tablasTemp)
        self.enroqueDerecho = enroque(torreTemp[0],torreTemp[1],torreTemp[2],torreTemp[3])

        return bestMove
    # por consola pa retificar
    def printAllMoveID(self, l):
        for move in l:
            print(move.moveID)
            v = self.MejoresJugadas()
            print(v)
        

    def MejoresJugadas(self):
        moves = self.getJugadasV()
        if not self.blancasTurno and self.mate:
            return math.inf
        elif self.blancasTurno and self.mate:
            return -math.inf
        elif self.tablas:
            return 0
        #esta parte no le miento profe sacadas de internet porque de ajedrez sabemos poco de jugadas buenas

        #Pawns
        wPjugada = [[ 0,  0,  0,  0,  0,  0,  0,  0],
                         [50, 50, 50, 50, 50, 50, 50, 50],
                         [10, 10, 20, 30, 30, 20, 10, 10],
                         [5,  5, 10, 25, 25, 10,  5, 5],
                         [0,  0,  0, 20, 20,  0,  0, 0],
                         [5, -5,-10,  0,  0,-10, -5,  5],
                         [5, 10, 10,-20,-20, 10, 10,  5],
                         [0,  0,  0,  0,  0,  0,  0,  0]]

        #Knights
        wNjugada = [[-50,-40,-30,-30,-30,-30,-40,-50],
                         [-40,-20,  0,  0,  0,  0,-20,-40],
                         [-30,  0, 10, 15, 15, 10,  0,-30],
                         [-30,  5, 15, 20, 20, 15,  5,-30],
                         [-30,  0, 15, 20, 20, 15,  0,-30],
                         [-30,  5, 10, 15, 15, 10,  5,-30],
                         [-40,-20,  0,  5,  5,  0,-20,-40],
                         [-50,-40,-30,-30,-30,-30,-40,-50]]

        #Bishops
        wBjugada = [[-20,-10,-10,-10,-10,-10,-10,-20],
                         [-10,  0,  0,  0,  0,  0,  0,-10],
                         [-10,  0,  5, 10, 10,  5,  0,-10],
                         [-10,  5,  5, 10, 10,  5,  5,-10],
                         [-10,  0, 10, 10, 10, 10,  0,-10],
                         [-10, 10, 10, 10, 10, 10, 10,-10],
                         [-10,  5,  0,  0,  0,  0,  5,-10],
                         [-20,-10,-10,-10,-10,-10,-10,-20]]

        #Rooks
        wRjugada = [[0,  0,  0,  0,  0,  0,  0,  0],
                        [ 5, 10, 10, 10, 10, 10, 10,  5],
                        [-5,  0,  0,  0,  0,  0,  0, -5],
                        [-5,  0,  0,  0,  0,  0,  0, -5],
                        [-5,  0,  0,  0,  0,  0,  0, -5],
                        [-5,  0,  0,  0,  0,  0,  0, -5],
                        [-5,  0,  0,  0,  0,  0,  0, -5],
                        [ 0,  0,  0,  5,  5,  0,  0,  0]]

        #Queens
        wQjugada = [[-20,-10,-10, -5, -5,-10,-10,-20],
                         [-10,  0,  0,  0,  0,  0,  0,-10],
                         [-10,  0,  5,  5,  5,  5,  0,-10],
                         [ -5,  0,  5,  5,  5,  5,  0, -5],
                         [  0,  0,  5,  5,  5,  5,  0, -5],
                         [-10,  5,  5,  5,  5,  5,  0,-10],
                         [-10,  0,  5,  0,  0,  0,  0,-10],
                         [-20,-10,-10, -5, -5,-10,-10,-20]]
        
        #King
        wKjugada = [[-30,-40,-40,-50,-50,-40,-40,-30],
                         [-30,-40,-40,-50,-50,-40,-40,-30],
                         [-30,-40,-40,-50,-50,-40,-40,-30],
                         [-30,-40,-40,-50,-50,-40,-40,-30],
                         [-20,-30,-30,-40,-40,-30,-30,-20],
                         [-10,-20,-20,-20,-20,-20,-20,-10],
                         [ 20, 20,  0,  0,  0,  0, 20, 20],
                         [ 20, 30, 10,  0,  0, 10, 30, 20]]
        
        bPjugada = self.JugadasPeroNegro(wPjugada)
        bNjugada = self.JugadasPeroNegro(wNjugada)
        bBjugada = self.JugadasPeroNegro(wBjugada)
        bRjugada = self.JugadasPeroNegro(wRjugada)
        bQjugada = self.JugadasPeroNegro(wQjugada)
        bKjugada = self.JugadasPeroNegro(wKjugada)
        
        values = {'wP': 100, 'wR':500, 'wN':300, 'wB':300, 'wQ':900, 'wK':20000,
                  'bP': -100, 'bR':-500, 'bN':-300, 'bB':-300, 'bQ':-900, 'bK':-20000}
        score = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece != '--':
                    score += values[self.board[r][c]]
                    if piece == 'wP':
                        score += wPjugada[r][c]
                    elif piece == 'bP':
                        score += bPjugada[r][c]
                    elif piece == 'wN':
                        score += wNjugada[r][c]
                    elif piece == 'bN':
                        score += bNjugada[r][c]
                    elif piece == 'wB':
                        score += wBjugada[r][c]
                    elif piece == 'bB':
                        score += bBjugada[r][c]
                    elif piece == 'wR':
                        score += wRjugada[r][c]
                    elif piece == 'bR':
                        score += bRjugada[r][c]
                    elif piece == 'wQ':
                        score += wQjugada[r][c]
                    elif piece == 'bQ':
                        score += bQjugada[r][c]
                    elif piece == 'wK':
                        score += wKjugada[r][c]
                    elif piece == 'bK':
                        score += bKjugada[r][c]
                
        return score


    def JugadasPeroNegro(self, l):
        lista = []
        for row in l:
            lista.insert(0,row)
        for r in range(8):
            for c in range(8):
                lista[r][c] = lista[r][c] * -1
                
        return lista
                   


class enroque():

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
    

class Move():
    # able to allow chess notation to python array location
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    
    def __init__(self, startSq, endSq, board, capturado = False, movimientoTorre = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.MoverPieza = board[self.startRow][self.startCol]
        self.capturaMemori = board[self.endRow][self.endCol]
        self.promocion = ((self.MoverPieza == 'wP' and self.endRow == 0) or (self.MoverPieza == 'bP' and self.endRow == 7))
        
        self.capturado = capturado
        if self.capturado:
            self.capturaMemori = 'wP' if self.MoverPieza == 'bP' else 'bP'
        self.movimientoTorre = movimientoTorre

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
    
    def getChessNot(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


