import os

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/depth_measurements.txt' % os.path.dirname(cwd)


def main():
    depth_measurements = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            depth_measurements.append(int(measure))

    greater_measurements = 0
    i = 1
    while i < len(depth_measurements):
        start = depth_measurements[i-1]
        end = depth_measurements[i]
        if start < end:
            greater_measurements += 1
        i += 1

    return greater_measurements


if __name__ == '__main__':
    print(main())
