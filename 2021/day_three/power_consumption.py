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


def build_bit_position_map(data):
    bit_length = len(data[0])
    position_map = {k: [] for k in range(bit_length)}

    for point in data:
        for index in range(bit_length):
            position_map[index].append(point[index])

    return position_map


def filter_points(points, bit_index, filter_by_value):
    # print(len(points))
    filtered_output = []
    for point in points:
        if point[bit_index] == filter_by_value:
            filtered_output.append(point)
    return filtered_output


def get_power_consumption():
    gamma_binary = ''
    binary_positions = get_binary_data()
    position_map = build_bit_position_map(binary_positions)

    for i, points in position_map.items():
        counter = Counter(points)
        most_common = counter.most_common(1)[0][0]
        gamma_binary += str(most_common)

    # invert binary
    epsilon_binary = ''.join(['1' if i == '0' else '0' for i in gamma_binary])

    # binary to int
    gamma_rate = int(gamma_binary, 2)
    epsilon_rate = int(epsilon_binary, 2)

    return gamma_rate * epsilon_rate


def get_life_support_rating():
    binary_positions = get_binary_data()

    filtered_positions = binary_positions.copy()
    for i in range(len(binary_positions[0])):
        position_map = build_bit_position_map(filtered_positions)
        counter = Counter(position_map[i])
        common_bits = counter.most_common(2)
        # If equally common, round up
        if common_bits[0][1] == common_bits[1][1]:
            most_common_bit = '1'
        else:
            most_common_bit = common_bits[0][0]
        filtered = filter_points(filtered_positions, i, most_common_bit)
        filtered_positions = filtered

        if len(filtered_positions) == 1:
            break

    filtered_positions_inverted = binary_positions.copy()
    for i in range(len(binary_positions[0])):
        position_map = build_bit_position_map(filtered_positions_inverted)
        counter = Counter(position_map[i])
        common_bits = counter.most_common(2)
        # If equally common, round down
        if common_bits[0][1] == common_bits[1][1]:
            least_common_bit = '0'
        else:
            least_common_bit = '1' if common_bits[0][0] == '0' else '0'
        filtered_inverted = filter_points(filtered_positions_inverted, i, least_common_bit)
        filtered_positions_inverted = filtered_inverted

        if len(filtered_positions_inverted) == 1:
            break

    # binary to int
    oxygen_rating = int(filtered_positions[0], 2)
    co2_rating = int(filtered_positions_inverted[0], 2)

    return oxygen_rating * co2_rating


def main():
    print(get_power_consumption())
    print(get_life_support_rating())


if __name__ == '__main__':
    main()
