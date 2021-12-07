import os

from pipeline.utils import contexts

cwd = os.getcwd()
measurement_data_file = '%s/puzzle_inputs/school_of_lanternfish.txt' % os.path.dirname(cwd)


def get_fish_data():
    fish_data = []
    with open(measurement_data_file) as f:
        for line in f.readlines():
            measure = line.split('\n')[0]
            fish = [int(f) for f in measure.split(',')]
            fish_data.extend(fish)

    return fish_data


def simulate_day(school):
    updated_school = []
    for fish in school:
        if fish == 0:
            updated_school.append(6)
            updated_school.append(8)
        else:
            updated_school.append(fish-1)
    return updated_school


def simulate_fish(days):
    school_of_fish = get_fish_data()
    for day in range(days):
        print('Day {}'.format(day))
        school_of_fish = simulate_day(school_of_fish)
        print('There are now {} lanternfish'.format(len(school_of_fish)))
    return len(school_of_fish)


def main():
    fish = 256
    with contexts.timed_test('simulte {} fish'.format(fish)):
        print(simulate_fish(fish))


if __name__ == '__main__':
    main()
