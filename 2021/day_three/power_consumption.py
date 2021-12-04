import os
from collections import Counter

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/binary_positions.txt' % os.path.dirname(cwd)


def get_binary_data():
    binary_positions = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            binary_positions.append(measure)

    return binary_positions


def main():
    gamma_binary = ''
    binary_positions = get_binary_data()
    bit_length = len(binary_positions[0])
    gamma_positions = {k: [] for k in range(bit_length)}

    for point in binary_positions:
        for index in range(bit_length):
            gamma_positions[index].append(point[index])

    for i, points in gamma_positions.items():
        counter = Counter(points)
        most_common = counter.most_common(1)[0][0]
        gamma_binary += str(most_common)

    # invert binary
    epsilon_binary = ''.join(['1' if i == '0' else '0' for i in gamma_binary])

    # binary to int
    gamma_rate = int(gamma_binary, 2)
    epsilon_rate = int(epsilon_binary, 2)

    return gamma_rate * epsilon_rate


if __name__ == '__main__':
    print(main())
