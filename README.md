# pentago
play pentago against a computer AI component

To start, navigate to the pentago directory and run the following command (requires python 2.7)

    $ python2 pentago.py ab 2 n
    
'ab' flag sets the computer AI to use the alpha/beta pruning algorithm. You can also use 'mm' for minimax, but this is not reccomended as it is much less performant. 

'2' specifies the number of levels deep into the decision tree the computer will search before making a move. Deeper levels make for a more challenging opponent, but require more CPU power

'n' tells the program to not run in diagnostic mode. 'y' will have more console output, like the number of nodes analyzed by the computer
