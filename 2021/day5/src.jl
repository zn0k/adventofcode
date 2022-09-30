using DataStructures

function processline(line)
    function toInt(val)
        return parse(Int, val)
    end
    start, _, stop = split(line)
    start_x, start_y = map(toInt, split(start, ','))
    stop_x, stop_y = map(toInt, split(stop, ','))
    return ((start_x, start_y), (stop_x, stop_y))
end

lines = map(processline, readlines(ARGS[1]))

function isstraight(line)
    (x1, y1), (x2, y2) = line
    if x1 == x2 || y1 == y2
        return true
    end
    return false
end

straightlines = filter(isstraight, lines)

# create a default dict to hold coordinates
# keys are coordinate tuples, values are the number of lines at this point
coordinates = DefaultDict{Tuple{Int, Int}, Int}(0)

# function to generate all the points on a line
function generatepoints(line)
    function createrange(start, stop)
        if start > stop
            return start:-1:stop
        else
            return start:stop
        end
    end

    # extract the coordinate parts
    (x1, y1), (x2, y2) = line
    # generate the ranges of x and y coordinates
    if x1 == x2     # horizontal line, repeat x and take ys from the input
        xs = fill(x1, abs(y2 - y1) + 1)
        ys = createrange(y1, y2)
    elseif y1 == y2 # vertical line, repeat y and take xs from the input
        xs = createrange(x1, x2)
        ys = fill(y1, abs(x2 - x1) + 1)
    else            # diagonal line, take ranges for x and y frmo the input
        xs = createrange(x1, x2)
        ys = createrange(y1, y2)
    end
    # zip them together to generate the points
    return zip(xs, ys)
end

# generate the points on all the straight lines
for line in straightlines
    for point in generatepoints(line)
        coordinates[point] += 1
    end
end

# pull out the points with overlaps, and count them
function count(d)
    return length(filter(kv -> kv.second > 1, coordinates))
end

overlaps = count(coordinates)
println("Solution 1: $overlaps")

# filter out the diagonals that haven't been mapped yet
# add them to the coordinates
diagonallines = filter(!isstraight, lines)
for line in diagonallines
    for point in generatepoints(line)
        coordinates[point] += 1
    end
end

overlaps = count(coordinates)
println("Solution 2: $overlaps")