writeup:

This challenge is actually solveable without N, it just takes 20m to run on a good computer. 
We chose to give a large multiple of N so you could instantiate the polynomial ring over Zmod(N) instead of over ZZ, making it run way faster.


The goal is to solve a constraint system modulo an uknown prime.
We can set two y value variables, and can then draw relations for each other unknown variable, dependent on the remaining x's, as well as those two y values.
Then we generate a bunch of constrains which should be zero to these two y values and the p value, and throw everything into a groebner basis :)
