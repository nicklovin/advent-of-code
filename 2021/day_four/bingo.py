import re
import os
from collections import Counter

cwd = os.getcwd()
bingo_cards_file = '%s/puzzle_inputs/bingo_cards.txt' % os.path.dirname(cwd)
bingo_inputs_file = '%s/puzzle_inputs/bingo_inputs.txt' % os.path.dirname(cwd)
# bingo_cards_file = r'C:\Users\Nick Love\AppData\Roaming\JetBrains\PyCharmCE2021.1\scratches\scratch_1.txt'
# bingo_inputs_file = r'C:\Users\Nick Love\AppData\Roaming\JetBrains\PyCharmCE2021.1\scratches\scratch_2.txt'

BINGO_ROW_PATTERN = r'(?P<row>\s*\d+\s+\d+\s+\d+\s+\d+\s+\d+)'


class BingoNumber(object):

    def __init__(self, number):
        self.number = number
        self._checked = False

    def __eq__(self, other):
        return other == self.number

    def __str__(self):
        return self.number

    def __int__(self):
        return int(self.number)

    def __repr__(self):
        return self.number

    def is_checked(self):
        return self._checked

    def set_checked(self, val):
        self._checked = val


class BingoCard(object):

    def __init__(self, rows):
        self.rows = []
        self.cols = [[], [], [], [], []]
        self.all_points = []
        self.set_rows(rows)
        self.set_cols()
        self.set_all_points()

    def __repr__(self):
        string_style = (
            '\t{0}\t{1}\t{2}\t{3}\t{4}\n'
            '\t{5}\t{6}\t{7}\t{8}\t{9}\n'
            '\t{10}\t{11}\t{12}\t{13}\t{14}\n'
            '\t{15}\t{16}\t{17}\t{18}\t{19}\n'
            '\t{20}\t{21}\t{22}\t{23}\t{24}\n'
        )
        return string_style.format(*self.all_points)

    def has_number(self, number):
        if number in self.all_points:
            return True

    def set_number_checked(self, number, check_state=True):
        index = self.all_points.index(number)
        self.all_points[index].set_checked(check_state)
        # Debug lines
        # if check_state:
        #     print('{} set to checked!'.format(number))
        # else:
        #     print('{} set to unchecked!'.format(number))

    def set_rows(self, inputs):
        for row in inputs:
            row_to_add = []
            for number in row:
                point = BingoNumber(number)
                row_to_add.append(point)
            self.rows.append(row_to_add)

    def set_cols(self):
        i = 0
        for row in self.rows:
            for index in range(5):
                self.cols[index].append(row[index])
            i += 1

    def set_all_points(self):
        for row in self.rows:
            for point in row:
                self.all_points.append(point)

    def check_for_bingo(self):
        i = 0
        for row in self.rows:
            bingo_row = True
            for checked in row:
                if not checked.is_checked():
                    bingo_row = False
                    break
            if bingo_row:
                return True, 'Row', i
            i += 1

        i = 0
        for col in self.cols:
            bingo_col = True
            for checked in col:
                if not checked.is_checked():
                    bingo_col = False
                    break
            if bingo_col:
                return True, 'Column', i
            i += 1

        return False, None, None

    def get_row(self, row):
        return self.rows[row]

    def get_col(self, col):
        return self.cols[col]

    def get_all_unmarked(self):
        unmarked = []
        for number in self.all_points:
            if not number.is_checked():
                unmarked.append(number)
        return unmarked


def remove_excess_whitespace(text):
    # Remove double spaces to prevent str.replace() breaking
    new_text = text.replace('  ', ' ')
    # Remove starting space for single digits
    if text.startswith(' '):
        new_text = new_text[1:]
    return new_text


def get_bingo_card_data():
    raw_data = []

    with open(bingo_cards_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            raw_data.append(measure)

    bingo_rows = []
    bingo_cards = []
    for chunk in raw_data:
        pattern_match = re.match(BINGO_ROW_PATTERN, chunk)
        if pattern_match:
            row_dict = pattern_match.groupdict()
            bingo_row = remove_excess_whitespace(row_dict['row'])
            bingo_rows.append(bingo_row.split(' '))
        else:
            bingo_card = BingoCard(bingo_rows)
            bingo_cards.append(bingo_card)
            bingo_rows = []
    # Last card may not have a blank line after
    if bingo_rows:
        bingo_card = BingoCard(bingo_rows)
        bingo_cards.append(bingo_card)

    enumerated_cards = dict(enumerate(bingo_cards))
    return enumerated_cards


def get_bingo_input_data():
    bingo_inputs = []
    with open(bingo_inputs_file) as f:
        input_numbers = f.readline()
        input_number = input_numbers.split(',')
        print(input_number[-1])
        input_number[-1].replace('\n', '')
        bingo_inputs = input_number

    return input_number


def find_first_winner():
    inputs = get_bingo_input_data()
    cards = get_bingo_card_data()

    # Many of these variables may be excess from earlier stream of consciousness, cleanup needed
    cross_type = ''
    winning_card = None
    winning_line = None
    bingo_found = False
    winners = []
    total_rounds = 0
    last_number = None
    for number in inputs:
        for i, card in cards.items():
            if card.has_number(number):
                card.set_number_checked(number, True)
            has_bingo, bingo_type, type_index = card.check_for_bingo()
            if has_bingo:
                bingo_found = True
                cross_type = bingo_type
                winning_card = card
                winning_line = type_index
                winner_str = 'Card {0}: {1} {2}'.format(i, bingo_type, type_index)
                winners.append(winner_str)
        total_rounds += 1
        if bingo_found:
            last_number = int(number)
            break

    win_msg = 'The following cards found bingo in {} rounds:\n'.format(total_rounds)
    win_msg += '\t{}'.format(','.join(winners))
    print(win_msg)
    # For prompt question, will fail on multiple winners for other methods
    return winning_card, cross_type, winning_line, last_number


def calculate_winning_score(card, cross_type, type_index, last_number):
    if cross_type.lower() == 'row':
        line = card.get_row(type_index)
    elif cross_type.lower() == 'column':
        line = card.get_col(type_index)
    else:
        raise KeyError('Invalid cross_type! {}'.format(cross_type))

    unmarked_sum = 0
    unmarked_numbers = card.get_all_unmarked()
    print(unmarked_numbers)
    for number in unmarked_numbers:
        unmarked_sum += int(number)

    return unmarked_sum * last_number


def main():
    card, cross_type, type_index, last_number = find_first_winner()
    print(calculate_winning_score(card, cross_type, type_index, last_number))


if __name__ == '__main__':
    main()
