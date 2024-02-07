/~ a simple code demonstration
for d'tilapia PL ~/
let a, b, c, i be int
let n_times, sum be int

print: "Number of times for this code to execute: "
input: n_times

// loop until it reaches n_times defined by the user
for i from 1 to n_times by 1 do:
    print: "Enter an integer: "
    input: a

    print: "Enter a second integer: "
    input: b

    print: "Enter a third integer: "
    input: c

    sum = a + b + c
    print: sum