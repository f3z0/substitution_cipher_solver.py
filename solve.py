import sys
from random import shuffle
import string
import re
import json

def reduce(s):
    symbols = list(string.ascii_lowercase)
    str_l = list(s)
    histo = dict((x, str_l.count(x)) for x in str_l)
    return "".join([symbols[histo[x]] for x in str_l])


def match_ct(key, str):
    r = len(re.findall(re.compile("[%s]" % "".join([k for k in key])), str))
    return r

def decipher(mapped_key, cipher):
    mapped_key[" "] = " "
    return "".join([mapped_key[l] for l in cipher])


def recurse_solve(mapped_key, cipher_txt_words_s2, plain_text_words, cipher_text):
    print "remaining words: %d" % len(cipher_txt_words_s2)
    if len(cipher_txt_words_s2) == 0:
        print "POSSIBLE: %s" % decipher(mapped_key, cipher_text)
        return plain_text_words
    cipher_txt_words_s2.sort(lambda x,y: cmp(match_ct(mapped_key,y), match_ct(mapped_key,x)))
    wrd2 = cipher_txt_words_s2[0]
    rgx2 = "^"
    has_unknown = False
    for letter in list(wrd2):
        if letter in mapped_key:
            rgx2 += mapped_key[letter]
        else:
            rgx2 += "[a-z]"
            has_unknown = True

    rgx2 += "$"

    if  has_unknown == False:
        plain_text_words_n = list(plain_text_words)
        plain_text_words_n.append(wrd2);
        plain_text_words.append(recurse_solve(mapped_key, list(cipher_txt_words_s2)[1:len(cipher_txt_words_s2)], plain_text_words_n, cipher_text))
        return plain_text_words


    words2 = [ line.strip() for line in open('./web2') if re.search(re.compile(rgx2), line)]
    words2 += [ line.strip()+"s" for line in open('./web2') if  re.search(re.compile(rgx2), line.strip()+"s")]
    words2 += [ line.strip()+"d" for line in open('./web2') if  re.search(re.compile(rgx2), line.strip()+"d")]
    words2 += [ line.strip()+"ed" for line in open('./web2') if  re.search(re.compile(rgx2), line.strip()+"ed")]

    print rgx2

    if len(words2) == 0:
        print "no match: %s" % len(words2)
        return None


    for w in words2:
        plain_text_words_n = list(plain_text_words)
        plain_text_words_n.append(w);
        z = dict(mapped_key.items() + dict((wrd2[i], w[i]) for i in range(0,len(w))).items())

        plain_text_words.append(recurse_solve(z, list(cipher_txt_words_s2)[1:len(cipher_txt_words_s2)], plain_text_words_n,cipher_text))

    return plain_text_words

def main():
    if sys.argv[1] == "e":
        symbols = list(string.ascii_lowercase)
        exclude = set(string.punctuation)
        plain_text = " ".join(sys.argv[2:len(sys.argv)]).lower()
        plain_text = list(''.join(ch for ch in plain_text if ch not in exclude))
        
        symbols_key = list(string.ascii_lowercase)
        shuffle(symbols_key)

        symbols.append(" ")
        symbols_key.append(" ")

        cipher = [(symbols_key[symbols.index(x)]) for x in plain_text]

        print "%s\n%s" % ("".join(cipher), "".join(symbols_key))
    elif sys.argv[1] == "d":

        cipher_txt_words = (" ".join(sys.argv[2:len(sys.argv)]).lower()).split(" ")
        cipher_txt_words_s = list(cipher_txt_words)

        cipher_txt_words_s.sort(lambda x,y: cmp(len(y), len(x)))

        wrd = cipher_txt_words_s[0]
        print "%s %d" % (wrd, len(wrd))
        print reduce(wrd)

        rgx = re.compile("^[a-z]{%d}$" % (len(wrd)))
        words = [ line.strip() for line in open('./web2') if re.search(rgx, line)]

        print "Found %d words of length %d" % (len(words), len(wrd))

        wrd_reduced = reduce(wrd)
        print (wrd_reduced == reduce('substituting'))
        words = [ w for w in words if reduce(w) == wrd_reduced]


        print "Found %d words matching pattern %s" % (len(words), wrd_reduced)

        for w in words:
            d = dict((wrd[i], w[i]) for i in range(0,len(w)))
            json.dumps(recurse_solve(d, list(cipher_txt_words_s)[1:len(cipher_txt_words_s)], [], " ".join(cipher_txt_words)))



if __name__ == "__main__":
    main()