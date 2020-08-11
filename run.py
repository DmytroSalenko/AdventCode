import types

import day_1, day_1_part_2, day_2, day_2_part_2, day_3, day_3_part_2, \
    day_4, day_4_part_2, day_5, day_5_part_2, day_7, day_9, day_9_part_2, \
    day_11, day_11_part_2

IGNORED_IMPORTS = ('builtins', 'types')


def get_days():
    days = []
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and \
                val.__name__ not in IGNORED_IMPORTS:
            days.append((val, val.__name__))
    return days


def show_choices():
    print('Please select the Day from the list:')
    for index, module_data in enumerate(get_days()):
        print('%d : %s' % (index, module_data[1]))


def run_solution(choice):
    try:
        index = int(choice)

        package_name = get_days()[index][0]
        print('Excellent choice! Getting result...')
        return package_name.solution()
    except (IndexError, ValueError):
        print('No solution found for the number entered')
        return None


if __name__ == '__main__':
    while True:
        show_choices()
        print('Enter your choice (enter 99 to quit):')
        choice = input()

        if choice == '99':
            break

        result = run_solution(choice)
        if result:
            print('Result is: %s' % result)

        print('Press Enter key to continue')
        input()



