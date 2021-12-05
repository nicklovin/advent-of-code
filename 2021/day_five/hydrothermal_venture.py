import os
import re

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/hydrothermal_vent_positions.txt' % os.path.dirname(cwd)
# measurement_data_file = r'C:\Users\Nick Love\AppData\Roaming\JetBrains\PyCharmCE2021.1\scratches\scratch_3.txt'


VENT_PATTERN = '(?P<x1>\d+),(?P<y1>\d+)\s+->\s+(?P<x2>\d+),(?P<y2>\d+)'


class VentLine(object):

    def __init__(self, vent_string):
        vents = re.match(VENT_PATTERN, vent_string)
        vent_dict = vents.groupdict()
        self.x1 = int(vent_dict['x1'])
        self.y1 = int(vent_dict['y1'])
        self.x2 = int(vent_dict['x2'])
        self.y2 = int(vent_dict['y2'])

        self._points = self._write_points()

    def is_straight(self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def _write_points(self):
        if not self.is_straight():
            return []  # Not Implemented, currently not needed
        if self.x1 == self.x2:
            # x = self.x1
            upper = self.y1 if self.y1 > self.y2 else self.y2
            lower = self.y1 if self.y1 < self.y2 else self.y2
            y = [(self.x1, point) for point in range(lower, upper+1)]
            return y
        if self.y1 == self.y2:
            # y = self.y1
            upper = self.x1 if self.x1 > self.x2 else self.x2
            lower = self.x1 if self.x1 < self.x2 else self.x2
            x = [(point, self.y1) for point in range(lower, upper+1)]
            return x

    def get_points(self):
        return self._points


class VentGrid(object):

    def __init__(self):
        self.points = {}

    def add_line(self, line):
        if isinstance(line, VentLine):
            line_points = line.get_points()
        else:
            line_points = line
        for point in line_points:
            formatted_point = '{0}-{1}'.format(point[0], point[1])
            if self.points.get(formatted_point):
                self.points[formatted_point] += 1
            else:
                self.points[formatted_point] = 1

    def get_most_dangerous_points(self):
        count = 0
        for val in self.points.values():
            if val > 1:
                count += 1
        return count


def get_vent_data():
    vent_data = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            vent_data.append(measure)

    return vent_data


def mark_dangerous_points():
    vent_data = get_vent_data()

    grid = VentGrid()
    for line in vent_data:
        vent_line = VentLine(line)
        grid.add_line(vent_line)
    return grid.get_most_dangerous_points()


def main():
    print(mark_dangerous_points())


if __name__ == '__main__':
    main()
