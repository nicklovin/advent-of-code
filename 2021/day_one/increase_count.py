import os

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/depth_measurements.txt' % os.path.dirname(cwd)


def get_measurement_data():
    depth_measurements = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            depth_measurements.append(int(measure))
    return depth_measurements


def get_raw_increasing_measurements():
    depth_measurements = get_measurement_data()
    greater_measurements = 0
    i = 1
    while i < len(depth_measurements):
        start = depth_measurements[i-1]
        end = depth_measurements[i]
        if start < end:
            greater_measurements += 1
        i += 1

    return greater_measurements


def get_sliding_increasing_measurements():
    depth_measurements = get_measurement_data()
    greater_measurements = 0
    i = 3
    while i < len(depth_measurements):
        data_a = depth_measurements[i-3]
        data_b = depth_measurements[i-2]
        data_c = depth_measurements[i-1]
        data_abc = data_a + data_b + data_c

        data_x = depth_measurements[i-2]
        data_y = depth_measurements[i-1]
        data_z = depth_measurements[i]
        data_xyz = data_x + data_y + data_z

        if data_abc < data_xyz:
            greater_measurements += 1
        i += 1

    return greater_measurements


def main():
    print(get_raw_increasing_measurements())
    print(get_sliding_increasing_measurements())


if __name__ == '__main__':
    main()
