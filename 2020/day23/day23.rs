fn main() {
    let result = play(10_000_000, 1_000_000);
    println!("Answer 2: {}", result);
}

fn play(rounds: usize, fill: usize) -> usize {
    let input = [3, 8, 9, 1, 2, 5, 4, 6, 7];
    // let input = [1, 5, 7, 6, 2, 3, 9, 8, 4];
    let mut cups = vec![0; fill + 1];
    //println!("cups are initialized to {:#?}", cups);

    for i in 0..input.len() - 1 {
        //println!("setting cups from input for index {}", i);
        cups[input[i]] = input[i + 1];
    }
    if fill > 9 {
        //println!("must fill up to {}", fill);
        for i in 9..fill {
            cups[i] = i + 1;
        }
        cups[fill] = input[0];
    } else {
        //println!("base case, wrap around last digit");
        cups[input[8]] = input[0];
    }
    //println!("cups are set to {:#?}", cups);
    
    let mut current = input[0];
    for _i in 0..rounds {
        let n = cups[current];
        let m = cups[n];
        let o = cups[m];
        let mut destination: usize;
        //println!("current is {}", current);
        if current > 1 {
            destination = current - 1;
        } else {
            destination = fill;
        }
        while (destination == n) || (destination == m) || (destination == o) {
            if destination > 1 {
                    destination = destination - 1;
            } else {
                destination = fill;
            }
        }
        cups[current] = cups[o];
        cups[o] = cups[destination];
        cups[destination] = n;
        current = cups[current];
        //println!("cups are {:#?}", cups);
    }

    let a = cups[1];
    let b = cups[a];
    a * b
}