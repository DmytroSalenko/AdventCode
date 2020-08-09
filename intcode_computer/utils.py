def parse_program(puzzle_input_file):
    """Parse the list of values from the input file"""
    sequence = []
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            sequence.extend([int(x) for x in line.split(',')])
    return sequence
