import functools

with open("input.txt", "r") as f:
    # read in the lines of the topography together with their list
    topo = [(index, line) for index, line in enumerate(f.read().split("\n"))]

print(
    sum(
        map(
            lambda (index, line): 1 if line[(index * 3) % len(line)] == "#" else 0
            , topo)))

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(
    # multiple all the tree counts
    functools.reduce(
        lambda x, y: x * y
        , map(
            # over all lines of a slope, sum up the trees seen
            lambda (right, lines): sum(
                map(
                    # check if a line contains a tree in the relevant position
                    # if so, replace the line with a 1, else with a 0
                    lambda (index, line): 1 if line[(index * right) % len(line)] == "#" else 0
                    , lines))
            , map(
                # for each slope, pull out the relevant lines
                lambda (right, down): (right, filter(
                    # check if line index divides cleanly by vertical step frequency
                    lambda (index, line): index % down == 0
                    , topo))
                , slopes))))