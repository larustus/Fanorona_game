# position - row, column
# color 0 - black, 1 - white

class Piece:
    def __init__(self, position, color):
        self.position = position
        self.color = color


class Board:
    def __init__(self, turn=1, pieces=None):
        if pieces is None:
            pieces = []
        self.pieces = pieces
        self.turn = turn
        self.board = [[0] * 9 for i in range(5)]

        for i in range(5):
            for j in range(9):
                if i < 2:
                    starting_piece = Piece([i, j], 0)
                    self.board[i][j] = starting_piece
                    self.pieces.append(starting_piece)
                elif i > 2:
                    starting_piece = Piece([i, j], 1)
                    self.board[i][j] = starting_piece
                    self.pieces.append(starting_piece)
                else:
                    if j < 4:
                        if j % 2 == 0:
                            starting_piece = Piece([i, j], 0)
                            self.board[i][j] = starting_piece
                            self.pieces.append(starting_piece)
                        else:
                            starting_piece = Piece([i, j], 1)
                            self.board[i][j] = starting_piece
                            self.pieces.append(starting_piece)
                    elif j > 4:
                        if j % 2 == 0:
                            starting_piece = Piece([i, j], 1)
                            self.board[i][j] = starting_piece
                            self.pieces.append(starting_piece)
                        else:
                            starting_piece = Piece([i, j], 0)
                            self.board[i][j] = starting_piece
                            self.pieces.append(starting_piece)
                    else:
                        starting_piece = Piece([i, j], ' ')
                        self.board[i][j] = starting_piece
                        self.pieces.append(starting_piece)

    def display_board(self):
        c = 0
        print('      0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8')
        print('--------------------------------------------------------')
        for i in range(5):
            print(c, end='   | ')
            for j in range(9):
                if j != 8:
                    print(str(self.board[i][j].color) + '  - ', end=' ')
                else:
                    print(str(self.board[i][j].color) + '  ', end=' ')
            print('')
            if c == 4:
                pass
            elif c % 2 == 0:
                print('    | |  \  |  /  |  \  |  /  |  \  |  /  |  \  |  /  | ')
            else:
                print('    | |  /  |  \  |  /  |  \  |  /  |  \  |  /  |  \  | ')
            c += 1

    def get_pieces_that_can_move(self):
        pieces_that_can_move = {}
        for i in self.pieces:
            if self.turn == i.color or i.color == 'g':
                pieces_that_can_move[i] = []
                if i.position[1] - 1 >= 0:
                    if self.board[i.position[0]][i.position[1] - 1].color == ' ':
                        pieces_that_can_move[i].append(self.board[i.position[0]][i.position[1] - 1])
                if i.position[1] + 1 < 9:
                    if self.board[i.position[0]][i.position[1] + 1].color == ' ':
                        pieces_that_can_move[i].append(self.board[i.position[0]][i.position[1] + 1])
                if i.position[0] - 1 >= 0:
                    if self.board[i.position[0] - 1][i.position[1]].color == ' ':
                        pieces_that_can_move[i].append(self.board[i.position[0] - 1][i.position[1]])
                if i.position[0] + 1 < 5:
                    if self.board[i.position[0] + 1][i.position[1]].color == ' ':
                        pieces_that_can_move[i].append(self.board[i.position[0] + 1][i.position[1]])

                if (i.position[0] % 2 == 0 and i.position[1] % 2 == 0) or \
                        (i.position[0] % 2 != 0 and i.position[1] % 2 != 0):
                    if i.position[0] - 1 >= 0 and i.position[1] - 1 >= 0:
                        if self.board[i.position[0] - 1][i.position[1] - 1].color == ' ':
                            pieces_that_can_move[i].append(self.board[i.position[0] - 1][i.position[1] - 1])
                    if i.position[0] - 1 >= 0 and i.position[1] + 1 < 9:
                        if self.board[i.position[0] - 1][i.position[1] + 1].color == ' ':
                            pieces_that_can_move[i].append(self.board[i.position[0] - 1][i.position[1] + 1])
                    if i.position[0] + 1 < 5 and i.position[1] - 1 >= 0:
                        if self.board[i.position[0] + 1][i.position[1] - 1].color == ' ':
                            pieces_that_can_move[i].append(self.board[i.position[0] + 1][i.position[1] - 1])
                    if i.position[0] + 1 < 5 and i.position[1] + 1 < 9:
                        if self.board[i.position[0] + 1][i.position[1] + 1].color == ' ':
                            pieces_that_can_move[i].append(self.board[i.position[0] + 1][i.position[1] + 1])

        real = {}
        for k in pieces_that_can_move:
            if len(pieces_that_can_move[k]) != 0:
                real[k] = pieces_that_can_move[k]
        return real

    # dostajemy slownik zetonow ktore maja wokol siebie wolne miejsca - wartosci slownika
    # teraz trzeba sprawdzic ktore z nich maja bicie - te ktore nie maja wyjebac, jesli zaden nie ma to dowolny ruch

    def check_if_pieces_that_can_move_can_attack(self, pieces_that_can_move):
        # current turn color and enemy_color
        current_color = self.turn
        if current_color == 1:
            enemy_color = 0
        else:
            enemy_color = 1

        # sprawdzam ktore maja bicie
        pieces_after_validation = {}
        # i = zeton z ruchami ; j = miejsce do ktorego moze isc
        for i in pieces_that_can_move:
            pieces_after_validation[i] = []
            for j in pieces_that_can_move[i]:
                chosen_piece_position = i.position
                goal_position = j.position

                # ten sam wiersz
                if chosen_piece_position[0] - goal_position[0] == 0:
                    # ruch w prawo
                    if chosen_piece_position[1] < goal_position[1]:
                        # podejscie pod zeton i odejscie od zetonu
                        if goal_position[1] + 1 < 9:
                            if self.board[goal_position[0]][goal_position[1] + 1].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                        # odejscie od zetonu
                        if goal_position[1] - 2 >= 0:
                            if j not in pieces_after_validation[i]:
                                if self.board[goal_position[0]][goal_position[1] - 2].color == enemy_color:
                                    pieces_after_validation[i].append(j)
                                    self.board[i.position[0]][i.position[1]].color = 'z'
                    # ruch w lewo
                    if chosen_piece_position[1] > goal_position[1]:
                        # podejscie pod zeton i odejscie od zetonu
                        if goal_position[1] - 1 >= 0:
                            if self.board[goal_position[0]][goal_position[1] - 1].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                        if goal_position[1] + 2 < 9:
                            if j not in pieces_after_validation[i]:
                                if self.board[goal_position[0]][goal_position[1] + 2].color == enemy_color:
                                    pieces_after_validation[i].append(j)
                                    self.board[i.position[0]][i.position[1]].color = 'z'
                # ta sama kolumna
                elif chosen_piece_position[1] - goal_position[1] == 0:
                    # ruch do gory
                    if chosen_piece_position[0] > goal_position[0]:
                        # podejscie pod zeton i odejscie od zetonu
                        if goal_position[0] - 1 >= 0:
                            if self.board[goal_position[0] - 1][goal_position[1]].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                        if goal_position[0] + 2 < 5:
                            if j not in pieces_after_validation[i]:
                                if self.board[goal_position[0] + 2][goal_position[1]].color == enemy_color:
                                    pieces_after_validation[i].append(j)
                                    self.board[i.position[0]][i.position[1]].color = 'z'
                    # ruch w dol
                    if chosen_piece_position[0] < goal_position[0]:
                        # podejscie pod zeton i odejscie od zetonu
                        if goal_position[0] + 1 < 5:
                            if self.board[goal_position[0] + 1][goal_position[1]].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                        if goal_position[0] - 2 >= 0:
                            if j not in pieces_after_validation[i]:
                                if self.board[goal_position[0] - 2][goal_position[1]].color == enemy_color:
                                    pieces_after_validation[i].append(j)
                                    self.board[i.position[0]][i.position[1]].color = 'z'
                # na ukos
                # ta sama ukosna / ruch do gory
                elif chosen_piece_position[0] - 1 == goal_position[0] and chosen_piece_position[1] + 1 == goal_position[1]:
                    # podejscie pod zeton
                    if goal_position[0] - 1 >= 0 and goal_position[1] + 1 < 9:
                        if self.board[goal_position[0] - 1][goal_position[1] + 1].color == enemy_color:
                            pieces_after_validation[i].append(j)
                            self.board[i.position[0]][i.position[1]].color = 'z'
                    # odejscie od zetonu
                    if goal_position[0] + 2 < 5 and goal_position[1] - 2 >= 0:
                        if j not in pieces_after_validation[i]:
                            if self.board[goal_position[0] + 2][goal_position[1] - 2].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                # ta sama ukosna / ruch do dolu
                elif chosen_piece_position[0] + 1 == goal_position[0] and chosen_piece_position[1] - 1 == goal_position[1]:
                    # podejscie pod zeton
                    if goal_position[0] + 1 < 5 and goal_position[1] - 1 >= 0:
                        if self.board[goal_position[0] + 1][goal_position[1] - 1].color == enemy_color:
                            pieces_after_validation[i].append(j)
                            self.board[i.position[0]][i.position[1]].color = 'z'
                    # odejscie od zetonu
                    if goal_position[0] - 2 >= 0 and goal_position[1] + 2 < 9:
                        if j not in pieces_after_validation[i]:
                            if self.board[goal_position[0] - 2][goal_position[1] + 2].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                # ta sama ukosna \ ruch do gory
                elif chosen_piece_position[0] - 1 == goal_position[0] and chosen_piece_position[1] - 1 == goal_position[1]:
                    # podejscie pod zeton
                    if goal_position[0] - 1 >= 0 and goal_position[1] - 1 >= 0:
                        if self.board[goal_position[0] - 1][goal_position[1] - 1].color == enemy_color:
                            pieces_after_validation[i].append(j)
                            self.board[i.position[0]][i.position[1]].color = 'z'
                    # odejscie od zetonu
                    if goal_position[0] + 2 < 5 and goal_position[1] + 2 < 9:
                        if j not in pieces_after_validation[i]:
                            if self.board[goal_position[0] + 2][goal_position[1] + 2].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
                # ta sama ukosna \ ruch do dolu
                elif chosen_piece_position[0] + 1 == goal_position[0] and chosen_piece_position[1] + 1 == goal_position[1]:
                    # podejscie pod zeton
                    if goal_position[0] + 1 < 5 and goal_position[1] + 1 < 9:
                        if self.board[goal_position[0] + 1][goal_position[1] + 1].color == enemy_color:
                            pieces_after_validation[i].append(j)
                            self.board[i.position[0]][i.position[1]].color = 'z'
                    # odejscie od zetonu
                    if goal_position[0] - 2 >= 0 and goal_position[1] - 2 >= 0:
                        if j not in pieces_after_validation[i]:
                            if self.board[goal_position[0] - 2][goal_position[1] - 2].color == enemy_color:
                                pieces_after_validation[i].append(j)
                                self.board[i.position[0]][i.position[1]].color = 'z'
        real = {}
        for k in pieces_after_validation:
            if len(pieces_after_validation[k]) != 0:
                real[k] = pieces_after_validation[k]

        # jesli nie ma bicia
        if len(real) == 0:
            for i in pieces_that_can_move:
                i.color = 'z'
            return pieces_that_can_move
        else:
            return real

    def get_possible_moves_for_piece(self, piece, pieces_that_can_move):
        # current turn color and enemy_color
        current_color = self.turn
        if current_color == 1:
            enemy_color = 0
        else:
            enemy_color = 1

        # ma znaczenie jesli ktos przeklikuje
        for row in self.board:
            for element in row:
                if element.color == 'g':
                    element.color = 'z'
                if element.color == 'x':
                    element.color = enemy_color

        # slownik atakowane pole - zbite zetony przez podejscie
        moveTo_attack_byApproaching = {}

        # slownik atakowane pole - zbite zetony przez odejscie
        moveTo_attack_byWithdrawal = {}

        # slownik - zeton ktory moze sie ruszyc ; pozycja na ktora moze sie ruszyc
        for i in pieces_that_can_move:
            # jesli kliknieto poprawny zeton - taki ktory ma ruchy
            if i.position == piece.position:
                self.board[i.position[0]][i.position[1]].color = 'g'

                for j in pieces_that_can_move[i]:
                    moveTo_attack_byWithdrawal[j] = []
                    moveTo_attack_byApproaching[j] = []
                    chosen_piece_position = i.position
                    goal_position = j.position

                    startingPiece_attackedPieces = {}

                    # ten sam wiersz
                    if chosen_piece_position[0] - goal_position[0] == 0:
                        # ruch w prawo
                        if chosen_piece_position[1] < goal_position[1]:
                            # podejscie pod zeton
                            x = 1
                            while goal_position[1] + x < 9:
                                if self.board[goal_position[0]][goal_position[1] + x].color == enemy_color:
                                    self.board[goal_position[0]][goal_position[1] + x].color = 'x'
                                    moveTo_attack_byApproaching[j].append(self.board[goal_position[0]][goal_position[1] + x])
                                    x += 1
                                else:
                                    break
                            # odejscie od zetonu
                            y = 2
                            while goal_position[1] - y >= 0:
                                if self.board[goal_position[0]][goal_position[1] - y].color == enemy_color:
                                    self.board[goal_position[0]][goal_position[1] - y].color = 'x'
                                    moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0]][goal_position[1] - y])
                                    y += 1
                                else:
                                    break
                        # ruch w lewo
                        if chosen_piece_position[1] > goal_position[1]:
                            # podejscie pod zeton
                            x = 1
                            while goal_position[1] - x >= 0:
                                if self.board[goal_position[0]][goal_position[1] - x].color == enemy_color:
                                    self.board[goal_position[0]][goal_position[1] - x].color = 'x'
                                    moveTo_attack_byApproaching[j].append(self.board[goal_position[0]][goal_position[1] - x])
                                    x += 1
                                else:
                                    break
                            # odejscie od zetonu
                            y = 2
                            while goal_position[1] + y < 9:
                                if self.board[goal_position[0]][goal_position[1] + y].color == enemy_color:
                                    self.board[goal_position[0]][goal_position[1] + y].color = 'x'
                                    moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0]][goal_position[1] + y])
                                    y += 1
                                else:
                                    break
                    # ta sama kolumna
                    elif chosen_piece_position[1] - goal_position[1] == 0:
                        # ruch do gory
                        if chosen_piece_position[0] > goal_position[0]:
                            # podejscie pod zeton
                            x = 1
                            while goal_position[0] - x >= 0:
                                if self.board[goal_position[0] - x][goal_position[1]].color == enemy_color:
                                    self.board[goal_position[0] - x][goal_position[1]].color = 'x'
                                    moveTo_attack_byApproaching[j].append(self.board[goal_position[0] - x][goal_position[1]])
                                    x += 1
                                else:
                                    break
                            # odejscie od zetonu
                            y = 2
                            while goal_position[0] + y < 5:
                                if self.board[goal_position[0] + y][goal_position[1]].color == enemy_color:
                                    self.board[goal_position[0] + y][goal_position[1]].color = 'x'
                                    moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] + y][goal_position[1]])
                                    y += 1
                                else:
                                    break
                        # ruch w dol
                        if chosen_piece_position[0] < goal_position[0]:
                            # podejscie pod zeton
                            x = 1
                            while goal_position[0] + x < 5:
                                if self.board[goal_position[0] + x][goal_position[1]].color == enemy_color:
                                    self.board[goal_position[0] + x][goal_position[1]].color = 'x'
                                    moveTo_attack_byApproaching[j].append(self.board[goal_position[0] + x][goal_position[1]])
                                    x += 1
                                else:
                                    break
                            # odejscie od zetonu
                            y = 2
                            while goal_position[0] - y >= 0:
                                if self.board[goal_position[0] - y][goal_position[1]].color == enemy_color:
                                    self.board[goal_position[0] - y][goal_position[1]].color = 'x'
                                    moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] - y][goal_position[1]])
                                    y += 1
                                else:
                                    break

                    # na ukos
                    # ta sama ukosna / ruch do gory
                    elif chosen_piece_position[0] - 1 == goal_position[0] and chosen_piece_position[1] + 1 == goal_position[1]:
                        # podejscie pod zeton
                        x = 1
                        while goal_position[0] - x >= 0 and goal_position[1] + x < 9:
                            if self.board[goal_position[0] - x][goal_position[1] + x].color == enemy_color:
                                self.board[goal_position[0] - x][goal_position[1] + x].color = 'x'
                                moveTo_attack_byApproaching[j].append(self.board[goal_position[0] - x][goal_position[1] + x])
                                x += 1
                            else:
                                break
                        # odejscie od zetonu
                        y = 2
                        while goal_position[0] + y < 5 and goal_position[1] - y >= 0:
                            if self.board[goal_position[0] + y][goal_position[1] - y].color == enemy_color:
                                self.board[goal_position[0] + y][goal_position[1] - y].color = 'x'
                                moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] + y][goal_position[1] - y])
                                y += 1
                            else:
                                break
                    # ta sama ukosna / ruch do dolu
                    elif chosen_piece_position[0] + 1 == goal_position[0] and chosen_piece_position[1] - 1 == goal_position[1]:
                        # podejscie pod zeton
                        x = 1
                        while goal_position[0] + x < 5 and goal_position[1] - x >= 0:
                            if self.board[goal_position[0] + x][goal_position[1] - x].color == enemy_color:
                                self.board[goal_position[0] + x][goal_position[1] - x].color = 'x'
                                moveTo_attack_byApproaching[j].append(self.board[goal_position[0] + x][goal_position[1] - x])
                                x += 1
                            else:
                                break

                        # odejscie od zetonu
                        y = 2
                        while goal_position[0] - y >= 0 and goal_position[1] + y < 9:
                            if self.board[goal_position[0] - y][goal_position[1] + y].color == enemy_color:
                                self.board[goal_position[0] - y][goal_position[1] + y].color = 'x'
                                moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] - y][goal_position[1] + y])
                                y += 1
                            else:
                                break
                    # ta sama ukosna \ ruch do gory
                    elif chosen_piece_position[0] - 1 == goal_position[0] and chosen_piece_position[1] - 1 == goal_position[1]:
                        # podejscie pod zeton
                        x = 1
                        while goal_position[0] - x >= 0 and goal_position[1] - x >= 0:
                            if self.board[goal_position[0] - x][goal_position[1] - x].color == enemy_color:
                                self.board[goal_position[0] - x][goal_position[1] - x].color = 'x'
                                moveTo_attack_byApproaching[j].append(self.board[goal_position[0] - x][goal_position[1] - x])
                                x += 1
                            else:
                                break

                        # odejscie od zetonu
                        y = 2
                        while goal_position[0] + y < 5 and goal_position[1] + y < 9:
                            if self.board[goal_position[0] + y][goal_position[1] + y].color == enemy_color:
                                self.board[goal_position[0] + y][goal_position[1] + y].color = 'x'
                                moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] + y][goal_position[1] + y])
                                y += 1
                            else:
                                break
                    # ta sama ukosna \ ruch do dolu
                    elif chosen_piece_position[0] + 1 == goal_position[0] and chosen_piece_position[1] + 1 == goal_position[1]:
                        # podejscie pod zeton
                        x = 1
                        while goal_position[0] + x < 5 and goal_position[1] + x < 9:
                            if self.board[goal_position[0] + x][goal_position[1] + x].color == enemy_color:
                                self.board[goal_position[0] + x][goal_position[1] + x].color = 'x'
                                moveTo_attack_byApproaching[j].append(
                                    self.board[goal_position[0] + x][goal_position[1] + x])
                                x += 1
                            else:
                                break
                        # odejscie od zetonu
                        y = 2
                        while goal_position[0] - y >= 0 and goal_position[1] - y >= 0:
                            if self.board[goal_position[0] - y][goal_position[1] - y].color == enemy_color:
                                self.board[goal_position[0] - y][goal_position[1] - y].color = 'x'
                                moveTo_attack_byWithdrawal[j].append(self.board[goal_position[0] - y][goal_position[1] - y])
                                y += 1
                            else:
                                break

        return moveTo_attack_byWithdrawal, moveTo_attack_byApproaching

    def move_piece(self, piece, clicked_space, moveTo_attack_byWithdrawal, moveTo_attack_byApproaching):
        # current turn color and enemy_color
        current_color = self.turn
        if current_color == 1:
            enemy_color = 0
        else:
            enemy_color = 1

        attacked_space = {clicked_space: []}

        # sprawdzic czy jest bicie
        temp = []
        for i in self.pieces:
            if i.color == 'x':
                temp.append(i)
        if len(temp) != 0:
            did_attack = True
            # najpierw sprawdzic jakie pole wybrano
            #jesli wybrano pole ktore jest w obydwu slownikach to trzeba wybrac ktore pola beda atakowane
            if len(moveTo_attack_byApproaching[clicked_space]) == 0 and len(moveTo_attack_byWithdrawal[clicked_space]) == 0:
                pass
            elif len(moveTo_attack_byWithdrawal[clicked_space]) == 0:
                attacked_space = moveTo_attack_byApproaching[clicked_space]
            elif len(moveTo_attack_byApproaching[clicked_space]) == 0:
                attacked_space = moveTo_attack_byWithdrawal[clicked_space]
            else:
                print('Choose which piece to attack')
                print('A - 0; W - 1\n')
                user_input = input()
                if user_input == '0':
                    attacked_space = moveTo_attack_byApproaching[clicked_space]
                else:
                    attacked_space = moveTo_attack_byWithdrawal[clicked_space]
        else:
            did_attack = False

        # zbicie pol atakowanych przez ruch
        for i in attacked_space:
            i.color = ' '


        # koniec wyswietlania mozliwosci ruchu i wybranego pola
        for row in self.board:
            for element in row:
                if element.color == 'z':
                    element.color = current_color
                if element.color == 'x':
                    element.color = enemy_color
        clicked_space.color = current_color
        piece.color = ' '

        return did_attack

    def check_end_game(self):
        if self.turn == 1:
            enemy_color = 0
        else:
            enemy_color = 1

        enemy_pieces = []
        for i in self.pieces:
            if i.color == enemy_color:
                enemy_pieces.append(i)
        return len(enemy_pieces)

    def check_if_more_moves(self, current_pos, used_spaces):
        for row in self.board:
            for element in row:
                if element.color == 'z':
                    element.color = self.turn
        current_pos.color = 'g'

        visited_places = used_spaces
        viable_space_for_attack = {}
        temp1 = self.get_pieces_that_can_move()
        temp2 = self.check_if_pieces_that_can_move_can_attack(temp1)
        if temp1 == temp2:
            temp2 = {current_pos: []}

        for k in temp2:
            print(k.position)
            for l in temp2[k]:
                print(l.position)
            print('--------')

        viable_space_for_attack[current_pos] = []
        # jesli obecna pozycja ma bicie
        if current_pos in temp2:
            for i in temp2[current_pos]:
                print(i.position)
                if i not in visited_places:
                    viable_space_for_attack[current_pos].append(i)

        for row in self.board:
            for element in row:
                if element.color == 'z':
                    element.color = self.turn
        current_pos.color = 'g'


        if len(viable_space_for_attack[current_pos]) != 0:
            w1, a1 = self.get_possible_moves_for_piece(current_pos, viable_space_for_attack)
            self.display_board()
            print('\n')

        # wybor pola na ktore sie przesunac z dostepnych
            available_places = []
            for i in w1.keys():
                available_places.append(i)
            for j in a1.keys():
                available_places.append(j)

            available_places = list(set(available_places))
            for i in available_places:
                print(i.position)
            choice = input('Choose 1, 2,...\n')
            new_pos = available_places[int(choice) - 1]


            self.move_piece(current_pos, new_pos, w1, a1)
            self.display_board()
            print('\n')
            used_spaces.append(current_pos)
            current_pos = new_pos

        # jesli obecna pozycja nie ma bicia
        else:
            used_spaces = []
            for row in self.board:
                for element in row:
                    if element.color == 'z':
                        element.color = self.turn
            current_pos.color = self.turn

        return used_spaces, current_pos

# # tworzy poczatkowe ustawienie
# board1 = Board()
# for i in board1.pieces:
#     i.color = '-'
# board1.pieces[0].color = 1
# board1.pieces[2].color = 1
# board1.pieces[5].color = 1
# board1.pieces[10].color = 1
# board1.pieces[12].color = 1
# board1.pieces[14].color = 0
# board1.pieces[16].color = 1
# board1.pieces[18].color = 1
# board1.pieces[20].color = 1
#
# board1.pieces[25].color = 0
# board1.pieces[27].color = 0
# board1.pieces[29].color = 0
# board1.pieces[32].color = 0
#
# board1.pieces[34].color = 0
# board1.pieces[36].color = 0
# board1.pieces[38].color = 0
# board1.pieces[40].color = 0
# board1.pieces[41].color = 0
# board1.display_board()
# # # # zbiera liste wszystkich zetonow ktore moga sie poruszyc
# t1 = board1.get_pieces_that_can_move()
# print('\n')
# t2 = board1.check_if_pieces_that_can_move_can_attack(t1)
# board1.display_board()
#
# withdrawal, approaching = board1.get_possible_moves_for_piece(board1.pieces[20], t2)
# print('\n')
# board1.display_board()
# print('\n')
#
#
# board1.move_piece(board1.pieces[20], board1.pieces[30], withdrawal, approaching)
# board1.display_board()
# print('\n')
#
#
# current_pos = board1.pieces[30]
# previous_pos = board1.pieces[20]
# used_spaces = [previous_pos]
#
# while len(used_spaces) != 0:
#     used_spaces, current_pos = board1.check_if_more_moves(current_pos, used_spaces)

# # 2 tura
# print('\n')
# board1.turn = 0
# t3 = board1.get_pieces_that_can_move()
# t4 = board1.check_if_pieces_that_can_move_can_attack(t3)
#
# # for i in t4:
# #     print(i.position)
# #     for j in t4[i]:
# #         print(j.position)
# #     print('------')
#
#

# board1 = Board()
# board1.display_board()


# board1.display_board()
# w2, a2 = board1.get_possible_moves_for_piece(board1.pieces[11], t4)
# print('\n')
# board1.display_board()
# board1.move_piece(board1.pieces[11], board1.pieces[20], w2, a2)
# print('\n')
# board1.display_board()


board1 = Board()
counter = 1
end_game = False
while not end_game:
    print("TURN " + str(counter) + ' - ' + str(board1.turn) + '\n')
    board1.display_board()
    print('\n')
    # if counter == 12:
    #     print('xd')
    t1 = board1.get_pieces_that_can_move()
    t2 = board1.check_if_pieces_that_can_move_can_attack(t1)
    board1.display_board()
    print('\n')
    # wybor zetonu z dostepnych
    available_pieces = []
    for i in t2.keys():
        available_pieces.append(i)
        print(i.position)
    choice = input('Choose 1, 2,...\n')
    piece = available_pieces[int(choice) - 1]
    w1, a1 = board1.get_possible_moves_for_piece(piece, t2)
    board1.display_board()
    print('\n')

    # wybor pola na ktore sie przesunac z dostepnych
    available_places = []
    for i in w1.keys():
        available_places.append(i)
    for j in a1.keys():
        available_places.append(j)

    available_places = list(set(available_places))
    for i in available_places:
        print(i.position)
    choice = input('Choose 1, 2,...\n')
    clicked_space = available_places[int(choice) - 1]
    did_attack = board1.move_piece(piece, clicked_space, w1, a1)
    if counter == 3:
        print('xd')

    used_spaces = [piece]

    print('\n')
    board1.display_board()

    if did_attack:
        while len(used_spaces) != 0:
            used_spaces, clicked_space = board1.check_if_more_moves(clicked_space, used_spaces)

    print('\n')
    board1.display_board()

    # check if end of game
    if board1.check_end_game() == 0:
        end_game = True

    if board1.turn == 1:
        board1.turn = 0
    else:
        board1.turn = 1
    counter += 1

if board1.turn == 1:
    winner = 1
else:
    winner = 0
print("THE WINNER IS:\n")
print(winner)