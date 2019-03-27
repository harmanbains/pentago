from sys import maxint

#this is the player class which holds info about each player and implements minimax and alphabeta
class Player:

    #we must pass in the color of the player, the algorithm used for searching, the depth,
    #whether or not to print diagnositic values, the player type if human, and the player name
    def __init__(self, color, algo, depth, diag, pType = "AI", name = "ShallowMind",):
    
        #initialize all parameters
        self.color = color
        self.algo = algo
        self.depth = int(depth)
        if diag == 'y':
            self.diag = True
        else:
            self.diag = False
        self.pType = pType
        self.name = name
        self.winner = None
        self.nodesOpen = 0
    
    #returns name of player
    def getName(self):
        return self.name
    
    #returns color of player
    def getColor(self):
        return self.color
    
    #returns the player's type ('AI' or 'Human')
    def getType(self):
        return self.pType 
        
    #returns the player's move, either by prompting a human player or implementing the chosen 
    #adverserial search algorithm
    def getMove(self, gameBoard):
        
        #if human, ask it
        if self.pType == 'Human':
            invalidMove = True
            while invalidMove:
                rawMove = raw_input("What is your move? (e.g. 2/4 3r ): ")
                move = (int(rawMove[0]), int(rawMove[2]), int(rawMove[4]), rawMove[5].lower())
                invalidMove = gameBoard.invalidMove(move)
                if invalidMove:
                    print 'Move is not valid'
            return (move)
        else:
            #else implement the desired adverserial search algorithm
            if self.algo == 'mm':
                return self.miniMax(gameBoard.getBoard(), self.depth)
            else:
                return self.alphaBeta(gameBoard.getBoard(), self.depth)
            
    #implements a general minimax algorithm from the given state to the given depth
    def miniMax(self, boardState, depth):
        move = None
        moveVal = None
        
        #get successor actions
        posActions = self.getActions(boardState)
        
        #for each action start the recursion
        for action in posActions:
            self.nodesOpen += 1
            #if it's the first action, update the move and top moveVal
            if move == None:
                move = action
                moveVal = self.minVal(self.result(boardState, action, self.getColor()), depth - 1)
            
            else:
                #else compair if the action is better than the previous best move and update accordingly
                tempVal = self.minVal(self.result(boardState, action, self.getColor()), depth - 1)
                if tempVal > moveVal:
                    move = action
                    moveVal = tempVal
        #if diag mode is 'y' the nodes expanded will be printed   
        if self.diag: print "Nodes Expanded: ", self.nodesOpen
        self.nodesOpen = 0
        return move
        
    #the maxVal which recursively returns the value of the node, up to the given depth or terminal state
    def maxVal(self, boardState, depth):
        #if at given depth, or at a terminal state it returns the utility
        if depth == 0 or self.gameOver(boardState):
            return self.utility(boardState)
        #otherwise it generates possible successors and recursively calls minVal and finds the best node
        posActions = self.getActions(boardState)
        v = maxint * -1
        for action in posActions:
            self.nodesOpen += 1
            v = max(v, self.minVal(self.result(boardState, action, self.getColor()), depth - 1))
        return v
    
    #the minVal which recursively returns the value of the node, up to the given depth or terminal state  
    def minVal(self, boardState, depth):
        #if at given depth, or at a terminal state it returns the utility
        if depth == 0 or self.gameOver(boardState):
            return self.utility(boardState)
        #otherwise it generates possible successors and recursively calls maxVal and finds the best node
        posActions = self.getActions(boardState)
        v = maxint
        for action in posActions:
            self.nodesOpen += 1
            v = min(v, self.maxVal(self.result(boardState, action, self.getColor()), depth - 1))
        return v
        
    #implements a minimax algorithm with alpha-beta pruning to the given depth
    def alphaBeta(self, boardState, depth):
        move = None
        moveVal = None
        #initializes alpha and beta to -infinity and +infinity respectively
        alpha = maxint * -1
        beta = maxint
        #generates all possible succesors and start the recursion
        posActions = self.getActions(boardState)
        for action in posActions:
            self.nodesOpen += 1
            #if it's the first action, update the move and top moveVal
            if move == None:
                move = action
                node =self.aBMinVal(self.result(boardState, action, self.getColor()), depth - 1, alpha, beta)
                #updates alpha
                if type(node) != int:
                    moveVal = node[0]
                    alpha = max(alpha, moveVal)
                else:
                    moveVal = node
                    alpha = max(alpha, moveVal)
                
            else:
                #else compair if the action is better than the previous best move and update accordingly
                node = self.aBMinVal(self.result(boardState, action, self.getColor()), depth - 1, alpha, beta)
                #updates alpha
                if type(node) != int:
                    tempVal = node[0]
                else:
                    tempVal = node
                
                if tempVal > moveVal:
                    move = action
                    moveVal = tempVal
                alpha = max(alpha, moveVal)
        
        #if diag mode is 'y' the nodes expanded will be printed           
        if self.diag: print "Nodes Expanded: ", self.nodesOpen
        self.nodesOpen = 0
        return move
        
    #the aBMaxVal which recursively returns the value of the node, up to the given depth or terminal state
    def aBMaxVal(self, boardState, depth, alpha, beta):
        #if at given depth, or at a terminal state it returns the utility
        if depth == 0 or self.gameOver(boardState):
            return self.utility(boardState)
        posActions = self.getActions(boardState)
        v = maxint * -1
        
        #otherwise it generates possible successors and recursively calls aBMaxVal and finds the best node, while also pruning if needed
        for action in posActions:
            self.nodesOpen += 1
            v = max(v, self.aBMinVal(self.result(boardState, action, self.getColor()), depth - 1, alpha, beta))
            if v >= beta:
                return (v, alpha, beta)
            alpha = max(alpha, v)
        return (v, alpha, beta)
    
    #the aBMinVal which recursively returns the value of the node, up to the given depth or terminal state
    def aBMinVal(self, boardState, depth, alpha, beta):
        #if at given depth, or at a terminal state it returns the utility
        if depth == 0 or self.gameOver(boardState):
            return self.utility(boardState)
        
        #otherwise it generates possible successors and recursively calls aBMinVal and finds the best node, while also pruning if needed
        posActions = self.getActions(boardState)
        v = maxint
        for action in posActions:
            self.nodesOpen += 1
            v = min(v, self.aBMaxVal(self.result(boardState, action, self.getColor()), depth - 1, alpha, beta))
            if v <= alpha:
                return (v, alpha, beta)
            beta = min(beta, v)
        return (v, alpha, beta)
    
    #returns the utility of the particular state
    def utility(self, boardState):
    
        myColor = self.getColor()
        opColor = None
        
        if myColor == 'w':
            opColor = 'b'
        else:
            opColor = 'w'
            
        #util for the player, the opponent, and the total (player - opponent)
        myUtil = 0
        opUtil = 0
        utilVal = 0
        
        #if there is already a winner, assign the appropriate value
        if self.winner != None:
            if self.winner == 't':
                return 0
            elif self.winner == myColor:
                return maxint
            else:
                return maxint * -1
        
        #else check each spot and append the utility for each piece to the respective player's utility
        for row in range(6):
            for column in range(6):
                #player's piece so myUtil is updated
                if boardState[row][column] == myColor:
                    tempUtil = self.pieceUtil(boardState, row, column, opColor)
                    myUtil += tempUtil
                #enemy piece so opUtil is updated
                elif boardState[row][column] == opColor:
                    tempUtil = self.pieceUtil(boardState, row, column, myColor)
                    opUtil += tempUtil
                       
            
        #the difference is returned
        utilVal = myUtil - opUtil
                        
        return utilVal
        
    #returns the utility of each piece on the board
    def pieceUtil(self, boardState, row, column, opColor):
        myUtil = 0
        checker = 1
        
        
                    
        #check the  column
        if row == 0:
            for checkRow in range(4):
                if boardState[checkRow + 1][column] != opColor:
                    checker += 1
                else:
                    checker = 1
                    break
        elif row == 5:
            for checkRow in range(4):
                if boardState[4 - checkRow][column] != opColor:
                    checker += 1
                else:
                    checker = 1
                    break
        else:
            checker = 0
            for checkRow in range(5):
                if boardState[checkRow][column] != opColor:
                    checker += 1
                else:
                    break
            if checker == 5:
                myUtil += 1
                if boardState[5][column] != opColor:
                    myUtil += 1
            checker = 1
            
        if checker == 5:
            myUtil += 1
            
        checker = 1
        
        #check the row
        if column == 0:
            for checkCol in range(4):
                if boardState[row][checkCol + 1] != opColor:
                    checker += 1
                else:
                    checker = 1
                    break
        elif column == 5:
            for checkCol in range(4):
                if boardState[row][4 - checkCol] != opColor:
                    checker += 1
                else:
                    checker = 1
                    break
        else:
            checker = 0
            for checkCol in range(5):
                if boardState[row][checkCol] != opColor:
                    checker += 1
                else:
                    break
            if checker == 5:
                myUtil += 1
                if boardState[row][5] != opColor:
                    myUtil += 1
            checker = 1
            
        if checker == 5:
            myUtil += 1
            
        checker = 1
            
        #check the top-lef to bottom-right corner
        if row == column:
            if row == 0:
                for checkDiag in range(4):
                    if boardState[checkDiag + 1][checkDiag + 1] != opColor:
                        checker += 1
                    else:
                        checker = 1
                        break
            elif row == 5:
                for checkDiag in range(4):
                    if boardState[4 - checkDiag][4 - checkDiag] != opColor:
                        checker += 1
                    else:
                        checker = 1
                        break
            else:
                checker = 0
                for checkDiag in range(5):
                    if boardState[checkDiag][checkDiag] != opColor:
                        checker += 1
                    else:
                        break
                if checker == 5:
                    myUtil += 1
                    if boardState[5][5] != opColor:
                        myUtil += 1
                checker = 1
        if checker == 5:
            myUtil += 1
            
        checker = 1
        
        #check the top-right to bottom left corner
        if row + column == 5:
            if row == 0:
                for checkDiag in range(4):
                    if boardState[checkDiag + 1][4 - checkDiag] != opColor:
                        checker += 1
                    else:
                        checker = 1
                        break
            elif row == 5:
                for checkDiag in range(4):
                    if boardState[4 - checkDiag][checkDiag + 1] != opColor:
                        checker += 1
                    else:
                        checker = 1
                        break
            else:
                checker = 0
                for checkDiag in range(5):
                    if boardState[checkDiag][5 - checkDiag] != opColor:
                        checker += 1
                    else:
                        break
                if checker == 5:
                    myUtil += 1
                    if boardState[5][0] != opColor:
                        myUtil += 1
                checker = 1
        if checker == 5:
            myUtil += 1
            
        checker = 0
        
        #check the top-left to bottom right outer diagonals
        if column - row == 1:
            for checkDiag in range(5):
                if boardState[checkDiag][checkDiag + 1] != opColor:
                    checker += 1
                else:
                    break
        elif row - column == 1:
            for checkDiag in range(5):
                if boardState[checkDiag + 1][checkDiag] != opColor:
                    checker += 1
                else:
                    break
        if checker == 5:
            myUtil += 1
            
        checker = 0
        
        #check the top-right to bottom left outer diagonals
        if column + row == 4:
            for checkDiag in range(5):
                if boardState[checkDiag][4 - checkDiag] != opColor:
                    checker += 1
                else:
                    break
        elif column + row == 6:
            for checkDiag in range(5):
                if boardState[checkDiag + 1][5 - checkDiag] != opColor:
                    checker += 1
                else:
                    break
        
        if checker == 5:
            myUtil += 1
            
        return myUtil
        
    #similar to the makeMove class in board.py
    #this function returns the successive state after the specified action is applied
    def result(self, boardState, action, theColor):
        tempBoard = []
        for row in range(6):
            tempBoard.append([])
            for column in range(6):
                tempBoard[row].append(boardState[row][column])
               
        if action[0] == 1:
            if action[1] == 1:
                tempBoard[0][0] = theColor
                    
            if action[1] == 2:
                tempBoard[0][1] = theColor
                    
            if action[1] == 3:
                tempBoard[0][2] = theColor
                    
            if action[1] == 4:
                tempBoard[1][0] = theColor
                    
            if action[1] == 5:
                tempBoard[1][1] = theColor
                    
            if action[1] == 6:
                tempBoard[1][2] = theColor
                    
            if action[1] == 7:
                tempBoard[2][0] = theColor
                    
            if action[1] == 8:
                tempBoard[2][1] = theColor
                    
            if action[1] == 9:
                tempBoard[2][2] = theColor
                    
        elif action[0] == 2:
            if action[1] == 1:
                tempBoard[0][3] = theColor
                    
            if action[1] == 2:
                tempBoard[0][4] = theColor
                    
            if action[1] == 3:
                tempBoard[0][5] = theColor
                    
            if action[1] == 4:
                tempBoard[1][3] = theColor
                    
            if action[1] == 5:
                tempBoard[1][4] = theColor
                    
            if action[1] == 6:
                tempBoard[1][5] = theColor
                    
            if action[1] == 7:
                tempBoard[2][3] = theColor
                    
            if action[1] == 8:
                tempBoard[2][4] = theColor
                    
            if action[1] == 9:
                tempBoard[2][5] = theColor
                    
        elif action[0] == 3:
            if action[1] == 1:
                tempBoard[3][0] = theColor
                    
            if action[1] == 2:
                tempBoard[3][1] = theColor
                    
            if action[1] == 3:
                tempBoard[3][2] = theColor
                    
            if action[1] == 4:
                tempBoard[4][0] = theColor
                    
            if action[1] == 5:
                tempBoard[4][1] = theColor
                    
            if action[1] == 6:
                tempBoard[4][2] = theColor
                    
            if action[1] == 7:
                tempBoard[5][0] = theColor
                    
            if action[1] == 8:
                tempBoard[5][1] = theColor
                    
            if action[1] == 9:
                tempBoard[5][2] = theColor
                    
        elif action[0] == 4:
            if action[1] == 1:
                tempBoard[3][3] = theColor
                    
            if action[1] == 2:
                tempBoard[3][4] = theColor
                    
            if action[1] == 3:
                tempBoard[3][5] = theColor
                    
            if action[1] == 4:
                tempBoard[4][3] = theColor
                    
            if action[1] == 5:
                tempBoard[4][4] = theColor
                    
            if action[1] == 6:
                tempBoard[4][5] = theColor
                    
            if action[1] == 7:
                tempBoard[5][3] = theColor
                    
            if action[1] == 8:
                tempBoard[5][4] = theColor
                    
            if action[1] == 9:
                tempBoard[5][5] = theColor
                    
        if self.gameOver(tempBoard):
            return tempBoard
        
        if action[3] == 'r':
            self.rotateQuadRight(action[2], tempBoard)
        else:
            self.rotateQuadLeft(action[2], tempBoard)
            
        return tempBoard
                
        
    #returns all legal actions from the given state
    def getActions(self, boardState):
        actions = []
        for row in range(6):
            for column in range(6):
                if boardState[row][column] == '.':
                    for quad in range(4):
                        if row == 0:
                            if column == 0:
                                actions.append((1, 1, quad + 1, 'l'))
                                actions.append((1, 1, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((1, 2, quad + 1, 'l'))
                                actions.append((1, 2, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((1, 3, quad + 1, 'l'))
                                actions.append((1, 3, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((2, 1, quad + 1, 'l'))
                                actions.append((2, 1, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((2, 2, quad + 1, 'l'))
                                actions.append((2, 2, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((2, 3, quad + 1, 'l'))
                                actions.append((2, 3, quad + 1, 'r'))
                        elif row == 1:
                            if column == 0:
                                actions.append((1, 4, quad + 1, 'l'))
                                actions.append((1, 4, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((1, 5, quad + 1, 'l'))
                                actions.append((1, 5, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((1, 6, quad + 1, 'l'))
                                actions.append((1, 6, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((2, 4, quad + 1, 'l'))
                                actions.append((2, 4, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((2, 5, quad + 1, 'l'))
                                actions.append((2, 5, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((2, 6, quad + 1, 'l'))
                                actions.append((2, 6, quad + 1, 'r'))
                        elif row == 2:
                            if column == 0:
                                actions.append((1, 7, quad + 1, 'l'))
                                actions.append((1, 7, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((1, 8, quad + 1, 'l'))
                                actions.append((1, 8, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((1, 9, quad + 1, 'l'))
                                actions.append((1, 9, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((2, 7, quad + 1, 'l'))
                                actions.append((2, 7, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((2, 8, quad + 1, 'l'))
                                actions.append((2, 8, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((2, 9, quad + 1, 'l'))
                                actions.append((2, 9, quad + 1, 'r'))
                        elif row == 3:
                            if column == 0:
                                actions.append((3, 1, quad + 1, 'l'))
                                actions.append((3, 1, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((3, 2, quad + 1, 'l'))
                                actions.append((3, 2, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((3, 3, quad + 1, 'l'))
                                actions.append((3, 3, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((4, 1, quad + 1, 'l'))
                                actions.append((4, 1, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((4, 2, quad + 1, 'l'))
                                actions.append((4, 2, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((4, 3, quad + 1, 'l'))
                                actions.append((4, 3, quad + 1, 'r'))
                        elif row == 4:
                            if column == 0:
                                actions.append((3, 4, quad + 1, 'l'))
                                actions.append((3, 4, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((3, 5, quad + 1, 'l'))
                                actions.append((3, 5, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((3, 6, quad + 1, 'l'))
                                actions.append((3, 6, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((4, 4, quad + 1, 'l'))
                                actions.append((4, 4, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((4, 5, quad + 1, 'l'))
                                actions.append((4, 5, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((4, 6, quad + 1, 'l'))
                                actions.append((4, 6, quad + 1, 'r'))
                        elif row == 5:
                            if column == 0:
                                actions.append((3, 7, quad + 1, 'l'))
                                actions.append((3, 7, quad + 1, 'r'))
                            elif column == 1:
                                actions.append((3, 8, quad + 1, 'l'))
                                actions.append((3, 8, quad + 1, 'r'))
                            elif column == 2:
                                actions.append((3, 9, quad + 1, 'l'))
                                actions.append((3, 9, quad + 1, 'r'))
                            elif column == 3:
                                actions.append((4, 7, quad + 1, 'l'))
                                actions.append((4, 7, quad + 1, 'r'))
                            elif column == 4:
                                actions.append((4, 8, quad + 1, 'l'))
                                actions.append((4, 8, quad + 1, 'r'))
                            elif column == 5:
                                actions.append((4, 9, quad + 1, 'l'))
                                actions.append((4, 9, quad + 1, 'r'))
        return actions
        
    #checks to see if the game is over
    def gameOver(self, boardState):
        whiteWin = False
        blackWin = False
        
        whiteCount = 0
        blackCount = 0
        
        #check each row
        for row in range(6):
        
            if boardState[row][0] == 'w':
                whiteCount = 1
                for column in range(4):
                    if boardState[row][column + 1] == 'w':
                        whiteCount += 1
                    else:
                        whiteCount = 0
                if whiteCount == 5:
                    whiteWin = True
            elif boardState[row][0] == 'b':
                blackCount = 1
                for column in range(4):
                    if boardState[row][column + 1] == 'b':
                        blackCount += 1
                    else:
                        blackCount = 0
                if blackCount == 5:
                    blackWin = True
                    
            if boardState[row][1] == 'w':
                whiteCount = 1
                for column in range(4):
                    if boardState[row][column + 2] == 'w':
                        whiteCount += 1
                    else:
                        whiteCount = 0
                if whiteCount == 5:
                    whiteWin = True
            elif boardState[row][1] == 'b':
                blackCount = 1
                for column in range(4):
                    if boardState[row][column + 2] == 'b':
                        blackCount += 1
                    else:
                        blackCount = 0
                if blackCount == 5:
                    blackWin = True
        
        #check each column           
        for column in range(6):
        
            if boardState[0][column] == 'w':
                whiteCount = 1
                for row in range(4):
                    if boardState[row + 1][column] == 'w':
                        whiteCount += 1
                    else:
                        whiteCount = 0
                if whiteCount == 5:
                    whiteWin = True
            elif boardState[0][column] == 'b':
                blackCount = 1
                for row in range(4):
                    if boardState[row + 1][column] == 'b':
                        blackCount += 1
                    else:
                        blackCount = 0
                if blackCount == 5:
                    blackWin = True
                    
            if boardState[1][column] == 'w':
                whiteCount = 1
                for row in range(4):
                    if boardState[row + 2][column] == 'w':
                        whiteCount += 1
                    else:
                        whiteCount = 0
                if whiteCount == 5:
                    whiteWin = True
            elif boardState[1][column] == 'b':
                blackCount = 1
                for row in range(4):
                    if boardState[row + 2][column] == 'b':
                        blackCount += 1
                    else:
                        blackCount = 0
                if blackCount == 5:
                    blackWin = True
        
        #check top-left to bottom-right diagonal            
        if boardState[0][0] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 1] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[0][0] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 1] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
        
        if boardState[1][1] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 2][coord + 2] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[1][1] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 2][coord + 2] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
        
        #check top-right to bottom-left diagonal        
        if boardState[0][5] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 1][4 - coord] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[0][5] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 1][4 - coord] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
        
        if boardState[1][4] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 2][3 - coord] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[1][4] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 2][3 - coord] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
                
        #check top-left to bottom-right outer diagonals
        if boardState[0][1] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 2] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[0][1] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 2] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
                    
        if boardState[1][0] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 2] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[1][0] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 1][coord + 2] == 'w':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
                
        #check top-right to bottom-left outer diagonals
        if boardState[0][4] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 1][3 - coord] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[0][4] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 1][3 - coord] == 'b':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
                    
        if boardState[1][5] == 'w':
            whiteCount = 1
            for coord in range(4):
                if boardState[coord + 2][4 - coord] == 'w':
                    whiteCount += 1
                else:
                    whiteCount = 0
            if whiteCount == 5:
                whiteWin = True
        elif boardState[1][5] == 'b':
            blackCount = 1
            for coord in range(4):
                if boardState[coord + 2][4 - coord] == 'w':
                    blackCount += 1
                else:
                    blackCount = 0
            if blackCount == 5:
                blackWin = True
        
                    
        if whiteWin and blackWin:
            self.winner = 't'
            return True
        elif whiteWin:
            self.winner = 'w'
            return True
        elif blackWin:
            self.winner = 'b'
            return True
            
        return False 
        
    #rotate the specified quadrant right
    def rotateQuadRight(self, quadrant, boardState):
        tempQuad = []
        
        if quadrant == 1:
            for row in range(3):
                tempQuad.append([])
                for column in range(3):
                    tempQuad[row].append(boardState[row][column])
            
            for row in range(3):
                for column in range(3):
                    boardState[row][column] = tempQuad[2 - column][row]
                    
        elif quadrant == 2:
            for row in range(3):
                tempQuad.append([])
                for column in range(3):
                    tempQuad[row].append(boardState[row][column + 3])

            for row in range(3):
                for column in range(3):
                    boardState[row][column + 3] = tempQuad[2 - column][row]
                    
        elif quadrant == 3:
            for row in range(3):
                tempQuad.append([])
                for column in range(3):
                    tempQuad[row].append(boardState[row + 3][column])
            
            for row in range(3):
                for column in range(3):
                    boardState[row + 3][column] = tempQuad[2 - column][row]
            
        elif quadrant == 4:
            for row in range(3):
                tempQuad.append([])
                for column in range(3):
                    tempQuad[row].append(boardState[row + 3][column + 3])
            
            for row in range(3):
                for column in range(3):
                    boardState[row + 3][column + 3] = tempQuad[2 - column][row]
                    
    #rotate the specified quadrant left
    def rotateQuadLeft(self, quadrant, boardState):
        self.rotateQuadRight(quadrant, boardState)
        self.rotateQuadRight(quadrant, boardState)
        self.rotateQuadRight(quadrant, boardState)
        
