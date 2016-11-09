import sys
from random import shuffle
import string
import re
import json
import time

lookup_cache = dict()

debug = 0

def dlog(s):
    if debug: print s

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

def construct_expression(wrd2, mapped_key):
    expr = "^"
    for letter in list(wrd2):
        if letter in mapped_key:
            expr += mapped_key[letter]
        else:
            expr += "[a-z]"
    return re.compile(expr + "$")

def get_possible_words(wrd, mapped_key):
    expr = construct_expression(wrd, mapped_key)
    if lookup_cache.has_key(expr.pattern):
        return lookup_cache[expr.pattern]
    
    words2 = [ line.strip() for line in open('./web2') if re.search(expr, line)]
    lookup_cache[expr.pattern] = words2
    return words2

def recurse_solve(mapped_key, cipher_txt_words_s2, cipher_text, l):
    if len(cipher_txt_words_s2) == 0:
        dlog("POSSIBLE: %s" % decipher(mapped_key, cipher_text))
        return decipher(mapped_key, cipher_text)
    
    cipher_txt_words_s2.sort(lambda x,y: cmp(match_ct(mapped_key,y), match_ct(mapped_key,x)))
    wrd2 = cipher_txt_words_s2[0]
    
    #if  has_unknown == False:
    #    plain_text_words_n = list(plain_text_words)
    #    plain_text_words_n.append(wrd2);
    #    plain_text_words.append(recurse_solve(mapped_key, list(cipher_txt_words_s2)[1:len(cipher_txt_words_s2)], plain_text_words_n, cipher_text, l+1))
    #    return []

    words2 = get_possible_words(wrd2, mapped_key)

    if len(words2) == 0:
        return None

    leftIndent = ""
    for i in range(0, l):
        leftIndent += "--"

    i = 0
    solutions = []
    for w in words2:
        dlog("%s %s (%d of %d)" % (leftIndent,w, i, len(words2)))
        #plain_text_words_n = list(plain_text_words)
        #plain_text_words_n.append(w);
        z = dict(mapped_key.items() + dict((wrd2[i], w[i]) for i in range(0,len(w))).items())

        solution = recurse_solve(z, list(cipher_txt_words_s2)[1:len(cipher_txt_words_s2)], cipher_text, l+1)
        if solution is not None: solutions.append(solution)
        dlog("%s /%s (%d of %d)" % (leftIndent,w, i, len(words2)))
        i += 1

    if len(solutions) == 0: return None

    return solutions

def flatten_solutions(a, b):
    if type(a) is type(''):
        b.append(a)
    elif type(a) is type([]):
        for x in a:
            flatten_solutions(x, b)

def main():
    start_time = time.time()
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

        solutions = []
        for w in words:
            dlog(w)
            d = dict((wrd[i], w[i]) for i in range(0,len(w)))
            solution = recurse_solve(d, list(cipher_txt_words_s)[1:len(cipher_txt_words_s)], " ".join(cipher_txt_words),1)
            if solution is not None: solutions.append(solution)
            dlog("/%s" % w)

        
        solutions_flat = []

        flatten_solutions(solutions, solutions_flat)
        print "Found %d total solutions in %f seconds." % (len(solutions_flat), time.time()-start_time)
        #for k in solutions_flat:
        #    print k


if __name__ == "__main__":
    main()