""" Крестики-нолики с компьютером """


class XOGame:
    def __init__(self):
        self.X_PLAYER = "X"
        self.O_PLAYER = "O"
        self.EMPTY = " "
        self.TIE = "Ничья"
        self.NUM_SQUARES = 9
        self.WAYS_TO_WIN = ((0, 1, 2),
                            (3, 4, 5),
                            (6, 7, 8),
                            (0, 3, 6),
                            (1, 4, 7),
                            (2, 5, 8),
                            (0, 4, 8),
                            (2, 4, 6),)
        self.board = []

    def display_instruction(self):
        """ Выводит инструкцию для игрока """
        print("""
        Добро пожаловать в игру 'Крестики-нолики'!
        Чтобы сделать ход, введи число от 0 до 8. Числа соответсвуют полям ниже:
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        Приготовьтесь к бою!\n 
        """)

    def ask_yes_no(self, question):
        """ Задает вопрос с ответом 'Да' или 'Нет' """
        response = None
        while response not in ('да', 'нет'):
            response = input(question).lower()
        return response

    def ask_number(self, question, low, high):
        """ Просит ввести число из диапазона """
        response = None
        while response not in range(low, high):
            response = int(input(question))
        return response

    def define_first_player(self):
        go_first = self.ask_yes_no("Хотите оставить за собой первый ход? Напишите 'да', если хотите:  ")
        if go_first.lower() == "да":
            print("\nНу, что ж, даю фору, играйте крестиками.")
            human = self.X_PLAYER
            computer = self.O_PLAYER
        else:
            human = self.O_PLAYER
            computer = self.X_PLAYER
        return human, computer

    def create_new_board(self):
        for square in range(self.NUM_SQUARES):
            self.board.append(self.EMPTY)

    def display_board(self):
        print("\n\t", self.board[0], "|", self.board[1], "|", self.board[2])
        print("\t", "---------")
        print("\n\t", self.board[3], "|", self.board[4], "|", self.board[5])
        print("\t", "---------")
        print("\n\t", self.board[6], "|", self.board[7], "|", self.board[8])

    def legal_moves(self):
        """Создать список доступных ходов"""
        moves = []
        for square in range(self.NUM_SQUARES):
            if self.board[square] == self.EMPTY:
                moves.append(square)
        return moves

    def choose_winner(self):
        """Определить победителя в игре"""
        for row in self.WAYS_TO_WIN:
            if self.board[row[0]] == self.board[row[1]] == self.board[row[2]] != self.EMPTY:
                # Если одинаковые фишки в позиции победы
                winner = self.board[row[0]]
                return winner
        if self.EMPTY not in self.board:
            return self.TIE
        else:
            return None

    def human_move(self):
        """Ход человека"""
        legal = self.legal_moves()
        move = None
        while move not in legal:
            move = self.ask_number("Твой ход, выбери поле (0, 8): ", 0, self.NUM_SQUARES)
            if move not in legal:
                print("\nСмешной человек! Это поле уже занято")
        print("Ладно...")
        return move

    def computer_move(self, computer, human):
        """Ход компьютера"""
        # Создаем копию доски, чтобы ничего не повредить
        board = self.board[:]
        BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
        print("Я выбираю номер: ", end=" ")
        # Проверяем все гипотетические ходы
        for move in self.legal_moves():
            board[move] = computer
            if self.choose_winner() == computer:
                print(move)
                return move
            # Убираем изменения
            board[move] = self.EMPTY
        for move in self.legal_moves():
            board[move] = human
            # Блокируем гипотетический выигрышный ход человека
            if self.choose_winner() == human:
                print(move)
                return move
            # Убираем изменения
            board[move] = self.EMPTY
        # Когда нет выигрыша на ближайшем ходу, выбираем из предпочтений
        for move in BEST_MOVES:
            if move in self.legal_moves():
                print(move)
                return move

    def next_turn(self, turn):
        if turn == self.X_PLAYER:
            return self.O_PLAYER
        else:
            return self.X_PLAYER

    def congrat_winner(self, the_winner, computer, human):
        if the_winner != self.TIE:
            print("Три ", the_winner, " в ряд!")
        else:
            print("Ничья!")
        if the_winner == computer:
            print("Я так и знал, человек! Твой интеллект слишком мал, чтобы победить!")
            return 'comp'
        elif the_winner == human:
            print("Не может быть! Это явно ошибка! Ты не мог этого сделать!",
                  "\n Клянусь, я больше такого не допущу!")
            return 'human'
        elif the_winner == self.TIE:
            print("Что ж, тебе удалось свести в ничью, но больше так не получится!")
            return 'tie'

    def game(self):
        self.display_instruction()
        human, computer = self.define_first_player()
        turn = self.X_PLAYER
        self.create_new_board()
        while not self.choose_winner():
            if turn == human:
                move = self.human_move()
                self.board[move] = human
            else:
                move = self.computer_move(computer, human)
                self.board[move] = computer
                self.display_board()
            turn = self.next_turn(turn)
        the_winner = self.choose_winner()
        winner = self.congrat_winner(the_winner, computer, human)
        return winner


if __name__ == '__main__':
    g = XOGame()
    s = g.game()
    print(s)