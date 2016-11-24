About
====================
Work-in-progress substitution cipher decryption. Instead of using differential techniques this project looks to seek ways to systemically reduce the keyspace using dictionary based attacks.

Usage
====================

### To generate a test cipher:

    $ python solve.py e  encryption is the process of encoding messages or information in such a way that only authorized parties can read it
    dfwyulknqf nr kjd lyqwdrr qa dfwqvnfp tdrropdr qy nfaqytoknqf nf rhwj o iou kjok qfzu ohkjqynedv loykndr wof ydov nk

### Attempt to break a cipher:

    $ python ./solve.py i #takes a few minutes

    $ python solve.py d dfwyulknqf nr kjd lyqwdrr qa dfwqvnfp tdrropdr qy nfaqytoknqf nf rhwj o iou kjok qfzu ohkjqynedv loykndr wof ydov nk

    encryption is the process of encoding messages or information in such a say that only authorized parties can read it
    encryption is the process of encoding messages or information in such a say that only authorised parties can read it
    encryption is the process of encoding messages or information in such a day that only authorized parties can read it
    encryption is the process of encoding messages or information in such a day that only authorised parties can read it
    encryption is the process of encoding messages or information in such a way that only authorized parties can read it
    encryption is the process of encoding messages or information in such a way that only authorised parties can read it
    encryption is the process of encoding messages or information in such a may that only authorized parties can read it
    encryption is the process of encoding messages or information in such a may that only authorised parties can read it
    encryption is the process of encoding messages or information in such a pay that only authorized parties can read it
    encryption is the process of encoding messages or information in such a pay that only authorised parties can read it
    encryption is the process of encoding messages or information in such a gay that only authorized parties can read it
    Found 32 total solutions in 6.610615 seconds.



Notes
====================

Requires the ciphertext to maintain the plaintext word breaks which is unrealistic.