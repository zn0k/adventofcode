using DelimitedFiles

readings = readdlm("input.txt", ',', Int, '\n')

answer1 = length(filter(t -> t[2] > t[1], collect(zip(readings, readings[2:end]))))
println("Answer 1: $(answer1)")

windows = map(sum, zip(readings, readings[2:end], readings[3:end]))
answer2 = length(filter(t -> t[2] > t[1], collect(zip(windows, windows[2:end]))))

println("Answer 2: $(answer2)")