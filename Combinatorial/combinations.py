"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Simple command line demonstration of combinatorial usage:

Use <<python>> combinations.py a:3 b:4 c:5 c=2 s=1

Where:
- <<name>>:<<number>> gives the dimension name and number of values
- c=<<number>> sets the coverage
- s=<<number>> sets the random seed

"""


if __name__ == '__main__':

    from sys import argv
    from combinatorials import Combinatorial, Dimension

    coverage = 0
    seed = None
    dimensions = []
    for arg in argv[1:]:
        if ':' in arg:
            name, features = arg.split(':')
            dimensions.append(Dimension(name, tuple(range(int(features)))))
        elif '=' in arg:
            setting, value = arg.split('=')
            if setting == 'c':
                coverage = int(value)
            elif setting == 's':
                seed = int(value)

    combinatorial = Combinatorial(dimensions, [], coverage, seed)
    count = 0
    for combination in combinatorial:
        print(combination)
        count += 1
    print(f'Count: {count} '
          f'({combinatorial.generator.minimum} - '
          f'{combinatorial.generator.maximum})')
