import random


class Guess:
    def __init__(self, dict_g_game):
        self.what_g = dict_g_game.get('what_guess')
        self.list_g = dict_g_game.get('list_guess').split(', ')
        self.choosen_value = random.choice(self.list_g)

    def game(self):
        print('Это игра на угадывание' + self.what_g + '. Ваша задача угадать сущность из следующего списка:')
        for elem in self.list_g:
            print(elem, end=" ")
        print('Сущность задана, поехали! У Вас три попытки.\n')

        for i in range(3):
            value = input('Ваш ответ: ')
            if value == self.choosen_value:
                print('Поздравляю, вы угадали!')
                return 1
            else:
                print('Мимо, у Вас еще ' + str(2-i) + ' попытки(-а).\n')
        else:
            print('К сожалению, Вы не угадали.')
            return 0


if __name__ == '__main__':
    s = {"what_guess": " числа", "list_guess": "1, 3, 5, 7, 8, 9, 10, 23, 14, 110"}
    g = Guess(s)
    a = g.game()
    print(a)


