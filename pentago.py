from player import Player
from board import Board
import sys


#This is the main which starts pentago. 3 Command line arguments are required
#the algorithm to be used (either 'ab' for alpha-beta or 'mm' minimax)
#the depth, I recommend no higher than 2
#if diagnostic values should be printed ('y' or 'n') This will print how many nodes are expanded
def main():
    
    # initialize the output file, gameboard, and command arguments
    f = open('output.txt', 'w')
    gameBoard = Board(f)
    nextPlayer = 1
    algorithm = sys.argv[1]
    depth = sys.argv[2]
    diag = sys.argv[3]
    
    #get player name
    print "Welcome to Pentago!"
    playerName = raw_input("What's your name?: ")
    
    validEntry = False
    
    #we keep looping until they provide a valid entry for player (1 or 2)
    while (not validEntry):
        playerSide = raw_input("Hey %s, which Player would you like to be? (1 or 2): " %(playerName))
        try:
            playerSide = int(playerSide)
        except ValueError:
            print "Invalid Entry Please Try Again!"
        else:
            if playerSide in (1, 2):
                validEntry = True
            else:
                print "Invalid Entry Please Try Again!"
 
    validEntry = False
    
    # we keep looping until they provide a valid entry for color ('w' or 'b')
    while (not validEntry):
        playerColor = raw_input("Which Color would you like to be? (w or b): ")
        if playerColor in ('w', 'W', 'b', 'B'):
            playerColor = playerColor.lower()
            validEntry = True
        else:
            print "Invalid Entry Please Try Again!"
    
    #now we initialize player1 and player2 based on the choices made, and the command-line arguments
    if playerSide == 1:
        player1 = Player(playerColor, algorithm, depth, diag, 'Human', playerName)
        if playerColor == 'w':
            player2 = Player('b', algorithm, depth, diag)
        else:
            player2 = Player('w', algorithm, depth, diag)
    else:
        player2 = Player(playerColor, algorithm, depth, diag, 'Human', playerName)
        if playerColor == 'w':
            player1 = Player('b', algorithm, depth, diag)
        else:
            player1 = Player('w', algorithm, depth, diag)
    
    #main loop which goes on until gameBoard.isGameOver() returns true
    while (not gameBoard.isGameOver()):
        #header to print out
        header = ''
        header += "\nPlayer 1 Name (player who moves first): " + player1.getName() + "\n"
        header += "Player 2 Name: " + player2.getName() + "\n"
        header += "Player 1 Token Color (b or w): " + player1.getColor() + "\n"
        header += "Player 2 Token Color (b or w): " + player2.getColor() + "\n"
        header += "Player to Move Next (1 or 2): " + str(nextPlayer) + "\n"
        f.write(header)
        print header
        gameBoard.printB()
        
        #get player moves
        if nextPlayer == 1:
            theMove = player1.getMove(gameBoard)
            gameBoard.makeMove(theMove, player1.getColor())
            nextPlayer = 2
        else:
            theMove = player2.getMove(gameBoard)
            gameBoard.makeMove(theMove, player2.getColor())
            nextPlayer = 1
    
    #print winner
    gameBoard.printB()
    print gameBoard.getWinner()
            
        
        
        
                 


if __name__ == '__main__':
    main()
