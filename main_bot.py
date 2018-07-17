
import json
from abc import ABCMeta, abstractmethod
from x_o_game import XOGame
from guess_game import Guess
import random
import datetime
from parser_news import Parser


def handler_answer(key, answer):
    if '-' in key:
        key1, key2 = key.split('-')
        if key1 in answer and key2 in answer.lower():
            return 1
    else:
        if key in answer.lower():
            return 1
        else:
            return 0


class State(metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, context):
        pass

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
    def to_parse_news(self, name):
        pass

    @abstractmethod
    def execution_state(self, context):
        pass


class GameState(State):
    def __init__(self, name_game):
        self.name_game = name_game
        self.list_states = [self.to_x_o_game, self.to_guess_game, self.to_parse_news]

    def set_state(self, context):
        self._context = context
        self._context.initial_first = False
        self.jokes = self._context.settings.get('joke_phrases')
        self.percent_wins = self._context.settings.get('percent_of_wins_bot')
        self.execution_state('')
        self.parser_answers()

    def parser_answers(self):
        print(self._context.settings.get('to_continue'))
        answer = input()
        for func in self.list_states:
            keys = self._context.settings.get('words_to_parse_answ').get(func.__name__)
            to_state = handler_answer(keys, answer)
            if func.__name__ == 'to_parse_news' and to_state:
                namegame = ''
                try:
                    index_beg_name = answer.index('"')
                    index_end_name = answer.rindex('"')
                    namegame = answer[index_beg_name + 1: index_end_name]
                except:
                    func('')
                else:
                    func(namegame)
            else:
                if to_state:
                    func()
        self._context.change_state(ErrorState())

    def to_x_o_game(self):
        self._context.change_state(XOGameState('x_o_game'))

    def to_guess_game(self):
        self._context.change_state(GuessGameState('guess_game'))

    def to_parse_news(self, name):
        self._context.change_state(ParserState(name))

    def execution_state(self, context):
        self.make_joke()
        result = self.start_game()
        self.write_result(result)
        self.parser_answers()

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
                if answer.lower() != 'да':
                    self._context.change_state(InitialState())

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
                logs.pop(index_name+1)
                logs.pop(index_name+1)
                logs.insert(index_name+1, 'human: ' + str(score_human))
                logs.insert(index_name+2, 'comp: ' + str(score_comp))

        # Для вставки данных игры, которой не было в логах,
        # необходимо открыть файл для дозаписи
        if name != '':
            with open('games_log.txt', 'a', encoding='utf-8') as log:
                log.write('\nname: ' + name + '\n')
                log.write('human: ' + str(score_human) + '\n')
                log.write('comp: ' + str(score_comp))
        # Для удаления старых значений - перезаписи
        else:
            with open('games_log.txt', 'w', encoding='utf-8') as log:
                for i in range(len(logs)):
                    if i == len(logs) - 1:
                        log.write(logs[i])
                    else:
                        log.write(logs[i] + '\n')


class XOGameState(GameState):
    def start_game(self):
        game = XOGame()
        winner = game.game()
        if winner == 'human':
            return 'human'
        elif winner == 'comp':
            return 'comp'


class GuessGameState(GameState):
    def start_game(self):
        dict_game = {'what_guess': self._context.settings.get('what_guess'),
                     'list_guess': self._context.settings.get('list_guess')}
        game = Guess(dict_game)
        winner = game.game()
        if winner == 'human':
            return 'human'
        elif winner == 'comp':
            return 'comp'


class ParserState(State):
    def __init__(self, name_game):
        self.name_game = name_game
        self.curr_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.type_r = 'news'
        self.list_states = [self.to_x_o_game, self.to_guess_game, self.to_parse_news]

    def set_state(self, context):
        self._context = context
        self._context.initial_first = False
        url = self._context.settings.get('base_url_news')
        self.execution_state(url)
        self.parser_answers()

    def parser_answers(self):
        print(self._context.settings.get('to_continue'))
        answer = input()
        for func in self.list_states:
            keys = self._context.settings.get('words_to_parse_answ').get(func.__name__)
            to_state = handler_answer(keys, answer)
            if func.__name__ == 'to_parse_news' and to_state:
                namegame = ''
                try:
                    index_beg_name = answer.index('"')
                    index_end_name = answer.rindex('"')
                    namegame = answer[index_beg_name + 1: index_end_name]
                except:
                    func('')
                else:
                    func(namegame)
            else:
                if to_state:
                    func()
        self._context.change_state(ErrorState())

    def to_x_o_game(self):
        self._context.change_state(XOGameState('x_o_game'))

    def to_guess_game(self):
        self._context.change_state(GuessGameState('guess_game'))

    def to_parse_news(self, name):
        self._context.change_state(ParserState(name))

    def execution_state(self, context):
        self.check_time()
        self.parse(context)
        self.parser_answers()

    def check_time(self):
        time_log = self.get_time_request()
        if time_log is not None:
            date, time = time_log.split(' - ')[1].split(': ')[1].split(' ')
            curr_date, curr_time = self.curr_time.split(' ')

            eq = self.eq_date(date, curr_date)
            if eq == 'same':
                fr = int(self._context.settings.get('frequency_req_min'))
                eq_t = self.eq_time(time, curr_time, fr)
                if eq_t == 'same':
                    print('Извините, вы не можете пока отправлять запросы на новости.'
                          ' Повторите через ' + str(fr) + ' минут.')
                    self._context.change_state(InitialState())

    def eq_time(self, time, curr_time, fr):
        h, m = time.split(':')
        h, m, = int(h), int(m)
        curr_h, curr_m = curr_time.split(':')
        curr_h, curr_m, = int(curr_h), int(curr_m)
        # От текущего времени отнимаем необходимый "отступ" для сверения
        if fr > 60:
            tmp_h = fr // 60
            curr_h -= tmp_h
            tmp_m = fr % 60
            if (curr_m - tmp_m) < 0:
                curr_h -= 1
                curr_m = 60 + (curr_m - tmp_m)
        else:
            if (curr_m - fr) < 0:
                curr_h -= 1
                curr_m = 60 + (curr_m - fr)
            else:
                curr_m -= fr

        if curr_h > h:
            return 'no'
        elif curr_h == h:
            if curr_m > m:
                return 'no'
            else:
                return 'same'

    def eq_date(self, date, curr_date):
        # проверка совпадения дат
        d, m, y = date.split('-')
        d, m, y = int(d), int(m), int(y)
        curr_d, curr_m, curr_y = curr_date.split('-')
        curr_d, curr_m, curr_y = int(curr_d), int(curr_m), int(curr_y)
        if y == curr_y:
            if m == curr_m:
                if d == curr_d:
                    return 'same'
        return 'no'

    def get_time_request(self):
        with open('parser_log.txt', 'r', encoding='utf-8') as log:
            logs = log.read().split('\n')
            if self.name_game == '':
                tmp = self.type_r
            else:
                tmp = self.type_r + " " + self.name_game
            for l in logs:
                if tmp in l:
                    return l
            return None

    def parse(self, base_url):
        pars = Parser(base_url, self.name_game)
        news = pars.get_news()
        for key, value in news.items():
            print('Заголовок: ' + value)
            print('Ссылка: ' + key)
        self.write_time()

    def write_time(self):
        time = self.get_time_request()
        str_time = 'type: ' + self.type_r + " " + self.name_game + ' - time: ' + self.curr_time
        if time is None:
            with open('parser_log.txt', 'a', encoding='utf-8') as log:
                log.write(str_time + '\n')
        else:
            logs = ''
            with open('parser_log.txt', 'r', encoding='utf-8') as log:
                logs = log.read().split('\n')
            with open('parser_log.txt', 'w', encoding='utf-8') as log:
                for l in logs:
                    if self.type_r in l:
                        log.write(str_time + '\n')
                    else:
                        log.write(l + '\n')


class InitialState(State):
    def __init__(self):
        self.list_states = [self.to_x_o_game, self.to_guess_game, self.to_parse_news]

    def set_state(self, context):
        self._context = context
        self._context.initial_first = False
        self.execution_state('')

    def parser_answers(self):
        print(self._context.settings.get('to_continue'))
        answer = input()
        for func in self.list_states:
            keys = self._context.settings.get('words_to_parse_answ').get(func.__name__)
            to_state = handler_answer(keys, answer)
            if func.__name__ == 'to_parse_news' and to_state:
                namegame = ''
                try:
                    index_beg_name = answer.index('"')
                    index_end_name = answer.rindex('"')
                    namegame = answer[index_beg_name + 1: index_end_name]
                except:
                    func('')
                else:
                    func(namegame)
            else:
                if to_state:
                    func()
        self._context.change_state(ErrorState())

    def execution_state(self, context):
        if self._context.initial_first:
            curr_intro = random.choice(self._context.settings.get('introduction_var'))
            print(curr_intro)
            for opport in self._context.settings.get('introduction_bot_opport'):
                print(opport)
        else:
            print(self._context.settings.get('introduction_again'))
            for opport in self._context.settings.get('introduction_bot_opport'):
                print(opport)
        self.parser_answers()

    def to_x_o_game(self):
        self._context.change_state(XOGameState('x_o_game'))

    def to_guess_game(self):
        self._context.change_state(GuessGameState('guess_game'))

    def to_parse_news(self, name):
        self._context.change_state(ParserState(name))


class ErrorState(State):
    def __init__(self):
        self.list_states = [self.to_x_o_game, self.to_guess_game, self.to_parse_news]

    def set_state(self, context):
        self._context = context
        self._context.initial_first = False
        self.execution_state('')

    def parser_answers(self):
        print(self._context.settings.get('to_continue'))
        answer = input()
        for func in self.list_states:
            keys = self._context.settings.get('words_to_parse_answ').get(func.__name__)
            to_state = handler_answer(keys, answer)
            if func.__name__ == 'to_parse_news' and to_state:
                namegame = ''
                try:
                    index_beg_name = answer.index('"')
                    index_end_name = answer.rindex('"')
                    namegame = answer[index_beg_name + 1: index_end_name]
                except:
                    func('')
                else:
                    func(namegame)
            else:
                if to_state:
                    func()
        self._context.change_state(ErrorState())

    def execution_state(self, context):
        print(self._context.settings.get('error_phrase'))
        self.parser_answers()

    def to_x_o_game(self):
        self._context.change_state(XOGameState('x_o_game'))

    def to_guess_game(self):
        self._context.change_state(GuessGameState('guess_game'))

    def to_parse_news(self, name):
        self._context.change_state(ParserState(name))


class Context:
    def __init__(self, file_set):
        self.path_file_settings = file_set
        self.settings = {}
        self.get_settings()
        self.initial_first = True
        self._state = self.change_state(InitialState())

    def change_state(self, new_state):
        self._state = new_state
        self._state.set_state(self)

    def get_settings(self):
        with open(self.path_file_settings, 'r', encoding='utf-8',) as f:
            data = json.loads(f.read())
            self.settings = data


if __name__ == '__main__':
    g = Context('settings.json')




