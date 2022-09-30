# read in the input file line by line
lines = readlines(ARGS[1])

# extract the draws and the boards
# for the draws, take the first line, split it on commas, and parse it to integers
draws = map(x -> parse(Int, x), split(lines[1], ','))
# determine the first time there's an empty line
chunk_size = findfirst(isequal(""), lines[3:end]) - 1
# for the boards, chunk lines 3 onward into segments of the appropriate size
boards = collect(Iterators.partition(lines[3:end], chunk_size + 1))
# then split those each on spaces
boards = map(x -> map(split, x[1:chunk_size]), boards)
# parse all the string numbers to integers
boards = map(x -> map(y -> map(z -> parse(Int, z), y), x), boards)
# turn the vector of vectors of vectors into a vector of 2-dimensional matrices
boards = map(x -> transpose(reduce(hcat, x)), boards)

# pre-calculate in what round each draw gets marked off
# create a dictionary that maps each draw to the round it is first drawn in
draw_scores = Dict(d => findfirst(isequal(d), draws) for d in Set(draws))

function get_round_board(board)
    # function to return the round during which a particular list of draws has been 
    # completely marked off
    function get_round_list(list)
        # map each value in the list to the round it would be first drawn in
        # default to infinity, so that a list that is never fully marked has that max value
        return maximum(map(x -> get(draw_scores, x, Inf), list))
    end

    # map each column, row, and diagonal to the round it would be completed in
    # return the minimum round, which is the first round in which a board wins
    lists = []
    append!(lists, eachcol(board), eachrow(board))
    return minimum(map(get_round_list, lists))
end

# map each board to the round in which it wins
winning_rounds = map(get_round_board, boards)

# function to select a board based on when it won
function select_board(f)
    round = f(winning_rounds)
    return (round, findfirst(isequal(round), winning_rounds))
end 

# find the first board that wins
first_winning_round, first_winning_board = select_board(minimum)

# function to score a board
function score_board(original_board, winning_round)
    # make a copy of the board
    board = copy(original_board)
    # go through the numbers that have been drawn up to the winning round
    # and filter them from the board
    for draw in draws[1:winning_round]
        replace!(board, draw => 0)
    end
    # sum up the remaining numbers and multiply them by the draw from the winning round
    return sum(board) * draws[winning_round]
end

solution1 = score_board(boards[first_winning_board], first_winning_round)
println("Solution 1: $solution1")

# find the last_board that wins
last_winning_round, last_winning_board = select_board(maximum)
solution2 = score_board(boards[last_winning_board], last_winning_round)
println("Solution 2: $solution2")
