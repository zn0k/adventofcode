using DelimitedFiles

# read in the binary strings, let collect chop them into chars
# then turn it all into a matrix via reduce/hcat, and rotate it right 90 degrees
# so that we can operate on columns efficiently
# lastly, convert the chars to integers
readings = map(x -> parse(Int, x), rotr90(reduce(hcat, map(collect, readdlm("input.txt", String)))))
# flip the matrix vertically, since we need to move left to right
readings = reverse(readings, dims=2)

function invert(val)
    return Int(!(Bool(val)))
end

# determine the bit value for a given column
function get_column_value(col, least_common = false)
    ones = count(x -> x == 1, col)
    zeroes = length(col) - ones
    result = (zeroes == ones || ones > zeroes) ? 1 : 0
    return least_common ? invert(result) : result
end

# function to convert a list of binary digits to a decimal number
# use big int for really large inputs
function bin2dec(bin)
    return parse(BigInt, join(bin); base=2)
end

function part1(matrix)
    gamma = []
    epsilon = []
    # go through each column
    for (index, col) in enumerate(eachcol(matrix))
        # find the column bit value
        val = get_column_value(col)
        # push the new binary digits for gamma and epsilon
        push!(gamma, val)
        push!(epsilon, invert(val))
    end
    return (bin2dec(gamma), bin2dec(epsilon))
end

(gamma, epsilon) = part1(readings)
println("Solution 1: $(gamma * epsilon)")

function part2(matrix)
    function select_column(matrix, least_common)
        index = 1
        # filter columns while there is more than one left
        while size(matrix, 1) > 1
            # get colunm at index, and get bit value for column
            col = matrix[:, index]
            val = get_column_value(col, least_common)
            # filter the matrix to the columns that have this value in that position
            matrix = matrix[matrix[:, index] .== val, :]
            # increase the column index
            index += 1
        end
        return matrix    
    end

    return (bin2dec(select_column(matrix, false)), bin2dec(select_column(matrix, true)))
end

(oxygen, co2) = part2(readings)
println("Solution 2: $(oxygen * co2)")