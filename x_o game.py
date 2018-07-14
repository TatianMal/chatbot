""" Крестики-нолики с компьютером """
# Global variables
X = "X"
O = "O"
EMPTY = " "
TIE = "Ничья"
NUM_SQUARES = 9


def display_instruct():
    """ Выводит инструкцию для игрока """
    print("""
    Добро пожаловать в игру 'Крестики-нолики'!
    Чтобы сделать ход, введи число от 0 до 8. Числа соответсвуют полям ниже:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    Приготовься к бою, белковое!\n 
    """)


def ask_yes_no(question):
    """ Задает вопрос с ответом 'Да' или 'Нет' """
    response = None
    while response not in ('y', 'n'):
        response = input(question).lower()
    return response


def ask_number(question, low, high):
    """ Просит ввести число из диапазона """
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response


def pieces():
    """ определяет, кто ходит первым """
    go_first = ask_yes_no("Хочешь оставить за собой первый ход? y - да, n - нет:  ")
    if go_first == "y":
        print("\nНу, что ж, даю фору, играй крестиками")
        human = X
        computer = O
    else:
        human = O
        computer = X
    return human, computer


def new_board():
    """ Создаем новую доску """
    board = []
    for square in range(NUM_SQUARES):
        board.append(EMPTY)
    return board


def display_board(board):
    """ Отобразить доску на экране """
    print("\n\t", board[0], "|", board[1], "|", board[2])
    print("\t", "---------")
    print("\n\t", board[3], "|", board[4], "|", board[5])
    print("\t", "---------")
    print("\n\t", board[6], "|", board[7], "|", board[8])


def legal_moves(board):
    """Создать список доступных ходов"""
    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:
            moves.append(square)
    return moves


def choose_winner(board):
    """Определить победителя в игре"""
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6),)
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            # Если одинаковые фишки в позиции победы
            winner = board[row[0]]
            return winner
    if EMPTY not in board:
        return TIE
    else:
        return None


def human_move(board, human):
    """Ход человека"""
    legal = legal_moves(board)
    move = None
    while move not in legal:
        move = ask_number("Твой ход, выбери поле (0, 8): ", 0, NUM_SQUARES)
        if move not in legal:
            print("\nСмешной человек! Это поле уже занято")
    print("Ладно...")
    return move


def computer_move(board, computer, human):
    """Ход компьютера"""
    # Создаем копию доски, чтобы ничего не повредить
    board = board[:]
    BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
    print("Я выбираю номер: ", end=" ")
    # Проверяем все гипотетические ходы
    for move in legal_moves(board):
        board[move] = computer
        if choose_winner(board) == computer:
            print(move)
            return move
        # Убираем изменения
        board[move] = EMPTY
    for move in legal_moves(board):
        board[move] = human
        # Блокируем гипотетический выигрышный ход человека
        if choose_winner(board) == human:
            print(move)
            return move
        # Убираем изменения
        board[move] = EMPTY
    # Когда нет выигрыша на ближайшем ходу, выбираем из предпочтений
    for move in BEST_MOVES:
        if move in legal_moves(board):
            print(move)
            return move


def next_turn(turn):
    if turn == X:
        return O
    else:
        return X


def congrat_winner(the_winner, computer, human):
    if the_winner != TIE:
        print("Три ", the_winner, " в ряд!")
    else:
        print("Ничья!")
    if the_winner == computer:
        print("Я так и знал, человек! Твой интеллект слишком мал, чтобы победить!")
    elif the_winner == human:
        print("Не может быть! Это явно ошибка! Ты не мог этого сделать!",
              "\n Клянусь, я больше такого не допущу!")
    elif the_winner == TIE:
        print("Что ж, тебе удалось свести в ничью, но больше так не получится!")


def main():
    display_instruct()
    human, computer = pieces()
    turn = X
    board = new_board()
    while not choose_winner(board):
        if turn == human:
            move = human_move(board, human)
            board[move] = human
        else:
            move = computer_move(board, computer, human)
            board[move] = computer
        display_board(board)
        turn = next_turn(turn)
    the_winner = choose_winner(board)
    congrat_winner(the_winner, computer, human)

main()
print("Спасибо за игру.")
input("\n\nНажмите Enter, чтобы выйти")