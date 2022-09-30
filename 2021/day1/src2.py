with open("input.txt", "r") as f:
    s=[int(l) for l in f]
f=lambda x: x[1]>x[0]
print(len(list(filter(f,zip(s,s[1:])))))
w=list(map(sum,zip(s,s[1:],s[2:])))
print(len(list(filter(f,zip(w,w[1:])))))