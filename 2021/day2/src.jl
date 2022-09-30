using DelimitedFiles

readings = readdlm("input.txt", ' ', '\n')

x = 0
y1 = 0
y2 = 0
for reading in eachrow(readings)
    if reading[1] == "forward"
        global x += reading[2]
        global y2 += y1 * reading[2]
    elseif reading[1] == "up"
        global y1 -= reading[2]
    elseif reading[1] == "down"
        global y1 += reading[2]
    end
end

answer1 = x * y1
answer2 = x * y2
println("Answer 1: $(answer1)")
println("Answer 2: $(answer2)")