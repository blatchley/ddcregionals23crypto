This is a challenge about fault injection in RSA.

A single bitflip in a variable in the signing process is enough to create faulty signatures, which can be used to leak the private key.

This is a very real world vulnerability, as biflips can be induced by messing with devices, or even just occur randomly due to cosmic radiation.
(fun video :) https://www.youtube.com/watch?v=AaZ_RSt0KP8)


You get to make 10 signatures on messages of your choosing,
Then you get to flip one bit in the stored key
then you get to make 10 more signautres until a fault is detected, at which point you need to decrypt a ciphertext.

First step, you don't know `N`. So you need to recover this somehow.

This can be done in the first 10 signatures.
If you get a signature on `3`, then a signature on `9`, you have two signatures of the form

(m=3) 
sg1 = m^d mod N 
sg2 = (m^2)^d mod N = m^2d mod N

this tells you that

sg1^2 = sg2 mod N

sg1^2 = sg2 + N * k for some integer k
sg1^2 - sg2 =  N * k for some integer k

So the difference between these two signatures is a multiple of N.

You could factor this and hope k has no large factors, but it's easiest ot just do this 4-5 times, and GCD all the results. As N is guarnateed to be in all of them.

Now that N is recovered, we get to flip a bit in the key.
The target here is going to bit flipping a bit in dq, This means the next signature is fault injected.
Lots of resources on this attack are available
https://www.cryptologie.net/article/371/fault-attacks-on-rsas-signatures/

This lets you factorise trivially, and you can decrypt the flag and win :)

