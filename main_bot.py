'''There will be a documentation'''
import json
from abc import ABCMeta, abstractmethod
from x_o_game import XOGame
from guess_game import Guess
import random
import datetime
from collections import OrderedDict
from parser import Parser


class State(metaclass=ABCMeta):
    # def __init__(self, Context):
    #     self.context = Context()

    @abstractmethod
    def parser_answers(self):
        pass

    @abstractmethod
    def to_x_o_game(self):
        pass

    @abstractmethod
    def to_guess_game(self):
        pass

    @abstractmethod
    def to_parse_news(self):
        pass

    @abstractmethod
    def to_parse_game_news(self):
        pass


class GameState(State):
    def __init__(self, joke_phrases, answer_phrase, percent_wins):
        self.name_game = ''
        self.jokes = joke_phrases
        self.answ_change_state = answer_phrase
        self.percent_wins = percent_wins

    def parser_answers(self):
        pass

    def to_x_o_game(self):
        pass

    def to_guess_game(self):
        pass

    def to_parse_news(self):
        pass

    def to_parse_game_news(self):
        pass

    def make_joke(self):
        '''Бот шутливо предлагает отказаться от игры, если до этого он побеждал
        определенное количество раз больше, чем человек'''
        sc_human, sc_comp = self.get_score()
        if sc_human != 0 or sc_comp != 0:
            coeff_wins = round(int(self.percent_wins) / 100, 1)
            compare_score = int(sc_human*(1 + coeff_wins))
            if sc_comp >= compare_score:
                curr_joke_phrase = random.choice(self.jokes)
                print(curr_joke_phrase)
                #  Да - вызвать метод игры, нет, вернуться в инициализацию
                answer = input()
                reason = self.parser_answers(answer)
                if reason:
                    self.start_game()
                # elif: переход к инициализации
                # else: переход в ошибке

    def start_game(self):
        pass

    def get_score(self):
        with open('games_log.txt', 'r', encoding='utf-8') as log:
            logs = log.read().split('\n')
            # Поиск имени игры. Если не найдено, то формируем лог с нуля. Найдено - переписываем лог
            try:
                index_name = logs.index('name: ' + self.name_game)
            except:
                return 0, 0
            else:
                score_human = int(logs[index_name+1].split(':')[1])
                score_comp = int(logs[index_name+2].split(':')[1])
                return score_human, score_comp

    def write_result(self, result):
        name = ''
        score_human = 0
        score_comp = 0
        logs = ''
        with open('games_log.txt', 'r', encoding='utf-8') as log:
            logs = log.read().split('\n')
            # Поиск имени игры. Если не найдено, то формируем лог с нуля. Найдено - переписываем лог
            try:
                index_name = logs.index('name: ' + self.name_game)
            except:
                name = self.name_game
                if result == 'human':
                    score_human = 1
                elif result == 'comp':
                    score_comp = 1
            else:
                score_human = int(logs[index_name+1].split(':')[1])
                score_comp = int(logs[index_name+2].split(':')[1])
                if result == 'human':
                    score_human += 1
                elif result == 'comp':
                    score_comp += 1
                logs.insert(index_name+1, 'human: ' + str(score_human))
                logs.insert(index_name+2, 'comp: ' + str(score_comp))

        # Для вставки данных игры, которой не было в логах,
        # необходимо открыть файл для дозаписи
        if name != '':
            with open('games_log.txt', 'a', encoding='utf-8') as log:
                log.write('name: ' + name + '\n')
                log.write('human: ' + str(score_human) + '\n')
                log.write('comp: ' + str(score_comp) + '\n')
        # Для удаления старых значений - перезаписи
        else:
            with open('games_log.txt', 'w', encoding='utf-8') as log:
                for line in logs:
                    log.write(line + '\n')


class XOGameState(GameState):
    def start_game(self):
        game = XOGame()
        winner = game.game()
        if winner == 'human':
            self.write_result('human')
        elif winner == 'comp':
            self.write_result('comp')


class GuessGameState(GameState):
    def start_game(self):
        game = Guess()
        winner = game.game()
        if winner == 'human':
            self.write_result('human')
        elif winner == 'comp':
            self.write_result('comp')


class ParserState(State):
    def __init__(self, answer_phrase):
        self.answ_change_state = answer_phrase
        self.curr_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    def parser_answers(self):
        #  Отсюда прислать и урл, и название игры
        pass

    def to_x_o_game(self):
        pass

    def to_guess_game(self):
        pass

    def to_parse_news(self):
        pass

    def to_parse_game_news(self):
        pass

    def get_time_request(self, type_req):
        with open('parser_log.txt', 'r', encoding='utf-8') as log:
            logs = log.read().split('\n')
            for l in logs:
                if type_req in l:
                    return l
            return None

    def parse(self, base_url, name_game):
        type = ''
        if name_game == '':
            type = 'news'
        else:
            type = 'news_about_game'
        pars = Parser(base_url, name_game)
        news = pars.get_news()
        for key, value in news.items():
            print('Заголовок: ' + value)
            print('Ссылка: ' + key)
            print('\n')
        self.write_time(type)

    def write_time(self, type):
        time = self.get_time_request(type)
        str_time = 'type: ' + type + 'time: ' + self.curr_time
        if time is None:
            with open('parser_log.txt', 'a', encoding='utf-8') as log:
                log.write(str_time + '\n')
        else:
            logs = ''
            with open('parser_log.txt', 'r', encoding='utf-8') as log:
                logs = log.read().split('\n')
            with open('parser_log.txt', 'w', encoding='utf-8') as log:
                for l in logs:
                    if type in l:
                        log.write(str_time + '\n')
                    else:
                        log.write(l + '\n')


class ParserNewsState(ParserState):
    pass


class ParserNewsGameState(ParserState):
    pass


class InitialState(State):
    def __init__(self, answer_phrase):
        self.answ_change_state = answer_phrase

    def parser_answers(self):
        pass
    # надо возвратить новый объект состояния????

    def to_x_o_game(self):
        pass

    def to_guess_game(self):
        pass

    def to_parse_news(self):
        pass

    def to_parse_game_news(self):
        pass


class ErrorState(State):
    def __init__(self, answer_phrase):
        self.answ_change_state = answer_phrase

    def parser_answers(self):
        pass

    def to_x_o_game(self):
        pass

    def to_guess_game(self):
        pass

    def to_parse_news(self):
        pass

    def to_parse_game_news(self):
        pass


class Context:
    def __init__(self, file_set):
        self.path_file_settings = file_set
        self.settings = {}
        self.initial_first = True
        self._state = InitialState()

    def change_state(self):
        self._state.parser_answers()

    def get_settings(self):
        with open(self.path_file_settings, 'r', encoding='utf-8',) as f:
            data = json.loads(f.read())
            self.settings = data


if __name__ == '__main__':
    g = Context(1, 'settings.json')
    g.get_settings()



