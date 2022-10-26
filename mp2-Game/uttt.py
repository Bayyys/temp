from time import sleep
from math import inf
from random import randint


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.maxDepth = 3
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        # self.startBoardIdx=randint(0,8)

        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.centerMaxUtility = 70
        self.sideMaxUtility = 50
        self.cornerMaxUtility = 30

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.centerMinUtility = -70
        self.sideMinUtility = -50
        self.cornerMinUtility = -30

        self.expandedNodes = 0
        self.currPlayer = True

        self.globalMoves = list(
            (x, y) for x in range(9) for y in range(9))  # list of all possible moves in global board
        self.localMoves = list((x, y) for x in range(3) for y in range(3))  # list of all possible moves in local board

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]]) + '\n' + '\n')
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]]) + '\n')
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]]) + '\n')

        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]]) + '\n')

    def twoInRow(self, isMax):
        """
        This function implements the count function for tow-in-row lines that two-sides did
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        mine(int): the number of two-in-row lines that player did
        yours(int): the number of two-in-row lines that opponent did
        """
        if isMax:
            player, opponent = 'X', 'O'
        else:
            player, opponent = 'O', 'X'
        mine, yours = 0, 0

        for x, y in self.globalIdx:
            x_list, row_list, col_list = [], [], []

            x_list.append([self.board[x][y], self.board[x + 1][y + 1], self.board[x + 2][y + 2]])
            x_list.append([self.board[x][y + 2], self.board[x + 1][y + 1], self.board[x + 2][y]])

            for row in range(3):
                row_list.append([self.board[x + row][y], self.board[x + row][y + 1], self.board[x + row][y + 2]])

            for col in range(3):
                col_list.append([self.board[x][y + col], self.board[x + 1][y + col], self.board[x + 2][y + col]])

            for list in x_list + row_list + col_list:
                if list.count(player) == 2 and list.count(opponent) == 0:
                    mine += 1
                elif list.count(player) == 0 and list.count(opponent) == 2:
                    yours += 1
        return mine, yours

    def corner(self, isMax):
        """
        This function implements the count function for corner points that player did
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        corners(int): the number of corner points that player did
        """
        if isMax:
            player = 'X'
        else:
            player = 'O'

        corners = 0
        for x, y in self.globalIdx:
            if self.board[x][y] == player:
                corners += 1
            if self.board[x][y + 2] == player:
                corners += 1
            if self.board[x + 2][y] == player:
                corners += 1
            if self.board[x + 2][y + 2] == player:
                corners += 1
        return corners

    def center(self, isMax):
        if isMax:
            player = 'X'
        else:
            player = 'O'

        center = 0
        for x, y in self.globalIdx:
            if self.board[x + 1][y + 1] == player:
                center += 1
        return center

    def side(self, isMax):
        if isMax:
            player = 'X'
        else:
            player = 'O'

        side = 0
        for x, y in self.globalIdx:
            if self.board[x][y + 1] == player:
                side += 1
            if self.board[x + 2][y + 1] == player:
                side += 1
            if self.board[x + 1][y] == player:
                side += 1
            if self.board[x + 1][y + 2] == player:
                side += 1
        return side

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # 1. three_in_row(winner)   2.two_in_row(mine+ yours-)    3.corner
        if isMax:
            if self.checkWinner() == 1:
                return self.winnerMaxUtility
            mine, yours = self.twoInRow(isMax)

            if mine or yours:
                return mine * self.twoInARowMaxUtility + yours * self.preventThreeInARowMaxUtility

            return self.corner(isMax) * self.cornerMaxUtility
        else:
            if self.checkWinner() == -1:
                return self.winnerMinUtility

            mine, yours = self.twoInRow(isMax)
            if mine or yours:
                return mine * self.twoInARowMinUtility + yours * self.preventThreeInARowMinUtility

            return self.corner(isMax) * self.cornerMinUtility

    def evaluateDesigned(self, isMax):
        # TODO: evaluateDesigned
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # 1. three_in_row(winner)   2.two_in_row & corner & center & side
        utility = 0
        if not isMax:
            if self.checkWinner() == 1:
                utility = float('inf')
                return utility

            if self.checkWinner() == -1:
                utility = -float('inf')
                return utility

            # two-in-a-row
            mine_unblocked, yours_blocked = self.twoInRow(isMax)
            if mine_unblocked or yours_blocked:
                utility += mine_unblocked * 200 + yours_blocked * 100

            yours_unblocked, mine_blocked = self.twoInRow(not isMax)
            if mine_unblocked or yours_blocked:
                utility += yours_unblocked * (-200) + mine_blocked * (-100)

            # corner
            utility += self.corner(isMax) * 30 + self.corner(not isMax) * (-30)

            # center
            utility += self.center(isMax) * 60 + self.center(not isMax) * (-60)

            # side
            utility += self.side(isMax) * 10 + self.side(not isMax) * (-10)

            return utility

        else:
            if self.checkWinner() == -1:
                utility = float('inf')
                return utility

            if self.checkWinner() == 1:
                utility = -float('inf')
                return utility

            # two-in-a-row
            mine_unblocked, yours_blocked = self.twoInRow(not isMax)
            if mine_unblocked or yours_blocked:
                utility += mine_unblocked * 200 + yours_blocked * 100

            yours_unblocked, mine_blocked = self.twoInRow(isMax)
            if mine_unblocked or yours_blocked:
                utility += yours_unblocked * (-200) + mine_blocked * (-100)

            # corner
            utility += self.corner(not isMax) * 30 + self.corner(isMax) * (-30)

            # center
            utility += self.center(not isMax) * 60 + self.center(not isMax) * (-60)

            # side
            utility += self.side(not isMax) * 10 + self.side(isMax) * (-10)

            return utility

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == '_':
                    return True
        return False

    def checkLocalLeft(self, Idx):
        """
        This function checks whether any local board is not finished.
        output:
        localLeft(bool): boolean variable indicates whether any local board is not finished.
        """
        for row in range(3):
            for col in range(3):
                if self.board[Idx[0] + row][Idx[1] + col] == '_':
                    return True
        return False

    def local2Global(self, Idx):
        """
        This function converts the local index to global index.
        input args:
        localIdx(tuple): local index
        output:
        globalIdx(tuple): global index
        """
        moves = list((x, y) for x in range(Idx[0], Idx[0] + 3) for y in range(Idx[1], Idx[1] + 3))
        return moves

    def checkWinner(self):
        # Return terminal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        for x, y in self.globalIdx:
            if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] != '_' \
                    or self.board[x][y + 2] == self.board[x + 1][y + 1] == self.board[x + 2][y] != '_':
                if self.board[x + 1][y + 1] == self.maxPlayer:
                    return 1
                else:
                    return -1

            for row in range(3):
                if self.board[x + row][y] == self.board[x + row][y + 1] == self.board[x + row][y + 2] != '_':
                    if self.board[x + row][y] == self.maxPlayer:
                        return 1
                    else:
                        return -1

            for col in range(3):
                if self.board[x][y + col] == self.board[x + 1][y + col] == self.board[x + 2][y + col] != '_':
                    if self.board[x][y + col] == self.maxPlayer:
                        return 1
                    else:
                        return -1
        return 0

    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        if depth == self.maxDepth:
            if self.currPlayer:
                return self.evaluatePredifined(isMax)
            else:
                return self.evaluateDesigned(isMax)

        if (isMax and depth == 1) or (not isMax and depth == 2):
            # maxPlayer's first move or minPlayer's second move
            # the situation where we look for the minimum value
            player = 'O'
            curr_best = float('inf')
        else:
            # minPlayer's first move or maxPlayer's second move
            # the situation where we look for the maximum value
            player = 'X'
            curr_best = -float('inf')

        if self.checkLocalLeft(self.globalIdx[currBoardIdx]):
            # if there are moves left in the local board
            moves = self.local2Global(self.globalIdx[currBoardIdx])  # get the global moves
        else:
            # if there are no moves left in the local board
            moves = self.globalMoves

        for i, j in moves:
            if self.board[i][j] != '_':
                # the move is not legal
                continue

            self.board[i][j] = player  # make the move
            self.expandedNodes += 1  # update the number of expanded nodes
            board_idx = self.getBoardIdx(i, j)  # update the local board index
            new_value = self.alphabeta(depth + 1, board_idx, alpha, beta, isMax)  # recursive call
            self.board[i][j] = '_'  # undo the move

            if (isMax and depth == 1) or (not isMax and depth == 2):
                curr_best = min(curr_best, new_value)
                if curr_best <= alpha:
                    return curr_best
                beta = min(beta, curr_best)

            else:
                curr_best = max(curr_best, new_value)
                if curr_best >= beta:
                    return curr_best
                alpha = max(alpha, curr_best)

        return curr_best

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        if depth == self.maxDepth:
            if self.currPlayer:
                return self.evaluatePredifined(isMax)
            else:
                return self.evaluateDesigned(isMax)

        if (isMax and depth == 1) or (not isMax and depth == 2):
            # maxPlayer's first move or minPlayer's second move
            # the situation where we look for the minimum value
            player = 'O'
            curr_best = float('inf')
        else:
            # minPlayer's first move or maxPlayer's second move
            # the situation where we look for the maximum value
            player = 'X'
            curr_best = float('-inf')

        if self.checkLocalLeft(self.globalIdx[currBoardIdx]):
            # if there are moves left in the local board
            moves = self.local2Global(self.globalIdx[currBoardIdx])  # get the global moves
        else:
            # if there are no moves left in the local board
            moves = self.globalMoves

        for i, j in moves:
            if self.board[i][j] != '_':
                # the move is not legal
                continue

            self.board[i][j] = player  # make the move
            self.expandedNodes += 1  # increase the number of expanded nodes
            board_idx = self.getBoardIdx(i, j)  # update the local board index
            new_value = self.minimax(depth + 1, board_idx, isMax)  # recursive call
            self.board[i][j] = '_'  # undo the move

            if (isMax and depth == 1) or (not isMax and depth == 2):
                # maxPlayer's first move or minPlayer's second move
                curr_best = min(curr_best, new_value)
            else:
                # minPlayer's first move or maxPlayer's second move
                curr_best = max(curr_best, new_value)

        return curr_best

    def getBoardIdx(self, best_x, best_y):
        """
        This function converts the global board index to boardIdx.
        input args:
        best_x(int): x coordinate of the move
        best_y(int): y coordinate of the move
        output:
        boardIdx(int): local board index
        """
        return (best_x % 3) * 3 + best_y % 3

    def playGamePredifinedAgent(self, maxFirst, isMinimaxOffensive, isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        bestMove = []  # list of bestMove coordinates at each step
        bestValue = []  # list of bestValue at each move

        if maxFirst:
            isMax = True  # maxPlayer plays first
        else:
            isMax = False  # minPlayer plays first

        if isMinimaxOffensive:
            offensive = self.minimax  # offensive agent uses minimax
        else:
            offensive = self.alphabeta  # offensive agent uses alpha-beta pruning

        if isMinimaxDefensive:
            defensive = self.minimax  # defensive agent uses minimax
        else:
            defensive = self.alphabeta  # defensive agent uses alpha-beta pruning

        board_idx = self.startBoardIdx  # current local board index

        while self.checkMovesLeft():
            # self.printGameBoard()  # debug: print current game board

            if self.checkWinner():
                # if there is a winner, break the loop
                break

            if isMax:
                # maxPlayer's turn
                player = 'X'
                algorithm = offensive
                curr_best = -float('inf')  # initialize bestValue to -infinity
            else:
                # minPlayer's turn
                player = 'O'
                algorithm = defensive
                curr_best = float('inf')  # initialize bestValue to infinity

            if self.checkLocalLeft(self.globalIdx[board_idx]):
                # if there are moves left in the local board
                best_x, best_y = self.globalIdx[board_idx]  # initialize bestMove to the first move in the local board
                moves = self.local2Global(self.globalIdx[board_idx])  # get the moves in the local board
            else:
                # if there are no moves left in the local board
                best_x, best_y = 0, 0  # initialize bestMove to the first move in the global board
                moves = self.globalMoves

            for i, j in moves:
                if self.board[i][j] != '_':
                    # check if the move is valid
                    continue

                self.board[i][j] = player  # make the move
                self.expandedNodes += 1  # increment the number of expanded nodes

                if algorithm == self.minimax:
                    new_value = algorithm(1, board_idx, isMax)  # call minimax
                else:
                    new_value = algorithm(1, board_idx, -float('inf'), float('inf'), isMax)  # call alphabeta

                if self.checkWinner():
                    curr_best = new_value  # update the current best value
                    best_x, best_y = i, j  # update the best move
                    break
                self.board[i][j] = '_'  # undo the move

                if isMax:
                    # maxPlayer's turn
                    if new_value > curr_best:  # check if the new value is better than the current best value
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move
                else:
                    # minPlayer's turn
                    if new_value < curr_best:  # check if the new value is better than the current best value
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move

            self.board[best_x][best_y] = player  # make the best move

            bestMove.append((best_x, best_y))  # append the best move to the list
            bestValue.append(curr_best)  # append the best value to the list

            isMax = not isMax  # switch the player
            board_idx = self.getBoardIdx(best_x, best_y)

        # self.printGameBoard()

        return self.board, bestMove, self.expandedNodes, bestValue, self.checkWinner()

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []  # list of bestMove coordinates at each step

        board_idx = randint(0, 8)  # randomize the current local board index
        isMax = randint(0, 1)  # randomize who plays first

        if isMax:
            player = 'X'  # agent's turn
        else:
            player = 'O'  # human's turn

        # print(f"从第{board_idx + 1}个棋盘开始，先行方为:" + player)

        if isMax:
            # agent plays first and use the predifined evaluation function
            self.currPlayer = True
        else:
            # human plays first and use the designed evaluation function
            self.currPlayer = False

        while self.checkMovesLeft():
            if self.checkWinner():
                # if there is a winner, break the loop
                break

            if isMax:
                player = 'X'  # agent's turn
                curr_best = -float('inf')  # initialize bestValue to -infinity
            else:
                player = 'O'  # human's turn
                curr_best = float('inf')  # initialize bestValue to infinity

            if self.checkLocalLeft(self.globalIdx[board_idx]):
                # if there are moves left in the local board
                best_x, best_y = self.globalIdx[board_idx]  # initialize bestMove to the first move in the local board
                moves = self.local2Global(self.globalIdx[board_idx])  # get the moves in the local board
            else:
                # if there are no moves left in the local board
                best_x, best_y = 0, 0  # initialize bestMove to the first move in the global board
                moves = self.globalMoves

            for i, j in moves:
                if self.board[i][j] != '_':
                    # check if the move is valid
                    continue

                self.board[i][j] = player  # make the move
                self.expandedNodes += 1  # increment the number of expanded nodes

                new_value = self.alphabeta(1, board_idx, -float('inf'), float('inf'), isMax)  # call alphabeta

                if self.checkWinner():
                    curr_best = new_value  # update the current best value
                    best_x, best_y = i, j  # update the best move
                    break
                self.board[i][j] = '_'  # undo the move

                if isMax:
                    if new_value > curr_best:
                        # check if the new value is better than the current best value
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move
                else:
                    if new_value < curr_best:
                        # check if the new value is better than the current best value
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move

            self.board[best_x][best_y] = player  # make the best move

            bestMove.append((best_x, best_y))  # append the best move to the list

            isMax = not isMax  # switch the player
            self.currPlayer = not self.currPlayer  # switch the evaluation function
            board_idx = self.getBoardIdx(best_x, best_y)  # update the local board index

        return self.board, bestMove, self.checkWinner()

    def playGameHuman(self):
        # TODO: playGameHuman
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        bestMove = []  # list of bestMove coordinates at each step

        board_idx = randint(0, 8)  # randomize the current local board index
        isMax = randint(0, 1)  # randomize who plays first
        self.currPlayer = False  # use the designed evaluation function

        print(f"从第{board_idx + 1}个棋盘开始，先行方为:" + ('Agent' if isMax else '人类玩家'))

        if isMax:
            player = 'X'  # agent's turn
        else:
            player = 'O'  # human's turn

        while self.checkMovesLeft():
            if self.checkWinner():
                # if there is a winner, break the loop
                break

            if isMax:
                player = 'X'  # agent's turn
                curr_best = -float('inf')  # initialize bestValue to -infinity

                if self.checkLocalLeft(self.globalIdx[board_idx]):
                    # if there are moves left in the local board
                    best_x, best_y = self.globalIdx[
                        board_idx]  # initialize bestMove to the first move in the local board
                    moves = self.local2Global(self.globalIdx[board_idx])  # get the moves in the local board
                else:
                    # if there are no moves left in the local board
                    best_x, best_y = 0, 0  # initialize bestMove to the first move in the global board
                    moves = self.globalMoves

                for i, j in moves:
                    if self.board[i][j] != '_':
                        # check if the move is valid
                        continue

                    self.board[i][j] = player  # make the move
                    self.expandedNodes += 1  # increment the number of expanded nodes

                    new_value = self.alphabeta(1, board_idx, -float('inf'), float('inf'), isMax)  # call alphabeta

                    if self.checkWinner():
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move
                        break
                    self.board[i][j] = '_'  # undo the move

                    if new_value > curr_best:
                        # check if the new value is better than the current best value
                        curr_best = new_value  # update the current best value
                        best_x, best_y = i, j  # update the best move
            else:  # human's turn
                player = 'O'  # agent's turn

                if self.checkLocalLeft(self.globalIdx[board_idx]):
                    # if there are moves left in the local board
                    print("当前棋盘为:")
                    self.printGameBoard()

                    print("当前棋盘可下的位置为:")
                    block = []
                    for x, y in self.local2Global(self.globalIdx[board_idx]):
                        if self.board[x][y] == '_':
                            block.append((x + 1, y + 1))
                    print(block)

                    print(f"请输入下一步的坐标(请放置在第{board_idx + 1}块棋盘上):")
                    best_x, best_y = map(int, input().split())

                    right_way = False
                    while not right_way:
                        if self.board[best_x][best_y] != '_':
                            print("该位置已经有棋子了, 请重新输入:")
                            best_x, best_y = map(int, input().split())
                        elif self.globalIdx[board_idx] != (best_x, best_y):
                            print("该位置不在当前棋盘上, 请重新输入:")
                            best_x, best_y = map(int, input().split())
                        else:
                            right_way = True

                else:
                    # if there are no moves left in the local board
                    print("当前棋盘为:")
                    self.printGameBoard()
                    print("请输入下一步的坐标(可放置在任一位置):")
                    best_x, best_y = map(int, input().split())
                    while self.board[best_x][best_y] != '_':
                        print("该位置已经有棋子了, 请重新输入:")
                        best_x, best_y = map(int, input().split())
            if isMax:
                self.board[best_x][best_y] = player  # make the agent's best move
            else:
                best_x, best_y = best_x - 1, best_y - 1
                self.board[best_x][best_y] = player  # make the human's best move
            bestMove.append((best_x, best_y))  # append the best move to the list

            isMax = not isMax  # switch the player
            board_idx = self.getBoardIdx(best_x, best_y)  # update the local board index

        return self.board, bestMove, self.checkWinner()


if __name__ == "__main__":
    # uttt = ultimateTicTacToe()
    # uttt.board = [['X', '_', 'X', '_', '_', '_', '_', '_', '_'],
    #               ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
    #               ['O', '_', 'X', '_', '_', '_', '_', '_', '_'],
    #               ['_', '_', '_', 'O', 'X', 'O', '_', '_', '_'],
    #               ['_', '_', '_', 'O', '_', 'X', '_', '_', '_'],
    #               ['_', '_', '_', 'X', 'O', 'O', '_', '_', '_'],
    #               ['O', '_', '_', '_', '_', '_', '_', '_', '_'],
    #               ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
    #               ['_', '_', '_', '_', '_', 'O', 'O', 'X', 'X']]
    # uttt.printGameBoard()
    # feel free to write your own test code
    # gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(True, True, True)
    # gameBoards, bestMove, winner = uttt.playGameHuman()
    # print(bestMove)
    # print(bestValue)
    # uttt.printGameBoard()
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")
    print("Run the UTTT task!!!!")
    print("Taks 1: Play with the evaluatePredifined x 4 times")
    print("Task 2: Play with the evaluateDesigned x 20 times")
    print("Task 3: Play with human x 10 times")
    task = input("Please input task number: ")

    if task == '1':
        for opponent, defense in ((True, True), (True, False), (False, True), (False, False)):
            uttt = ultimateTicTacToe()
            gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(opponent, opponent, defense)
            print("---------------------The divider---------------------")
            print(f"opponent: " + ("Minimax" if opponent else "Alpha-beta") + f"  VS  defense: " + ("Minimax" if opponent else "Alpha-beta"))
            uttt.printGameBoard()
            print(f"expandedNodes: {expandedNodes}")
            print(f"And the winner is" + (" maxPlayer" if winner == 1 else " minPlayer") + "!!!")

    elif task == "2":
        times = int(input("Choose the times of the match:"))
        win = 0
        print("running")
        for i in range(times):
            uttt = ultimateTicTacToe()
            gameBoards, bestMove, winner = uttt.playGameYourAgent()
            if winner == -1:
                win += 1
            print(f"Run the {i + 1} times...    " + f"and the winner is " + ('PredifinedAgent' if (winner == 1) else ("Tie" if (winner == 0) else "YourAgent")) + f"    " + f"and your agent win {win} / {(i + 1)} times")

        print("In 100 games, your agent winning times:")
        print(win)

    elif task == "3":
        pass

    else:
        print("Wrong input")
        exit(0)
