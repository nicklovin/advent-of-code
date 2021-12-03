import os

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/dive_movements.txt' % os.path.dirname(cwd)


def get_movement_data():
    dive_movements = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            dive_movements.append(measure)

    return dive_movements


def get_final_positions():
    depth = 0
    distance = 0
    dive_movements = get_movement_data()
    print(dive_movements)

    for movement in dive_movements:
        movement_type, delta = movement.split(' ')
        if movement_type == 'up':
            depth -= int(delta)
        elif movement_type == 'down':
            depth += int(delta)
        elif movement_type == 'forward':
            distance += int(delta)

    return distance, depth


def main():
    x, y = get_final_positions()
    return x * y


if __name__ == '__main__':
    print(main())
