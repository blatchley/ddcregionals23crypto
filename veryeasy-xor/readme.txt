You are given the encryption of two known messages, both appended with the flag.

The known prefixes differ in length by one.

If the prefix of m1 is A long, and the prefix of m2 is B = A-1 long

We can use the prefix of m1 to leak the A'th byte of the key, use that to decrypt hte first byte of the flag. Then append this newly learned byte to the known prefix of m1 (because it also has the flag next,) and use that to derive the A+1'th byte of the key, and use that to decrypt the second bye of the flag. Repeat this til entire flag is leraned :)

