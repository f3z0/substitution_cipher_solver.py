About
====================
Work-in-progress substitution cipher decryption. Instead of using differential techniques this project looks to seek ways to systemically reduce the keyspace using dictionary based attacks. It's currently very basic, I will soon be adding markov chains so the algorithm can predict and skip improbable sentence fragments. Also the reduce function is only used on the first word, however in theory it could be used for every word to decrease the key space even further.

Usage
====================

### To generate a test cipher:

python ./solve.py e In cryptography, a classical cipher is a type of cipher that was used historically but now has fallen, for the most part, into disuse.


### Attempt to break a cipher:

python ./solve.py e th rqegkjxqmgye m romnntrmo rtgyfq tn m kegf ji rtgyfq kymk smn lnfz ytnkjqtrmooe ulk hjs ymn imoofh ijq kyf ajnk gmqk thkj ztnlnf
murzfixytpvoahjgcqnklbsdew

Notes
====================

It sometimes gets stuck for long periods at local minima, I have some ideas on how to resolve this. In the meantime if you see it generate a word which is mostly unknowns ^e[a-z]ar[a-z][a-z][a-z]$ best to manually remove it from the cipher text and allow it to solve the rest which you can then use to substitute/solve the problematic word.


Disclaimer: Substitution ciphers can be broken in seconds using letter frequency matching and other differential methods, this is obviously not a secure encryption algorithm and is intended for education/entertainment purposes only.	